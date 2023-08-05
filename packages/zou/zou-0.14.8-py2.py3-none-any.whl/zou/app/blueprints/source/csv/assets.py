from zou.app.blueprints.source.csv.base import (
    BaseCsvProjectImportResource,
    RowException,
)
from zou.app.models.project import ProjectTaskTypeLink
from zou.app.models.task_type import TaskType

from zou.app.services import assets_service, projects_service, shots_service
from zou.app.models.entity import Entity
from zou.app.services.tasks_service import (
    create_task,
    create_tasks,
    get_tasks_for_asset,
    get_task_statuses,
    get_task_type,
)
from zou.app.services.comments_service import create_comment
from zou.app.services.persons_service import get_current_user
from zou.app.utils import events


class AssetsCsvImportResource(BaseCsvProjectImportResource):
    def prepare_import(self, project_id):
        self.episodes = {}
        self.entity_types = {}
        self.descriptor_fields = self.get_descriptor_field_map(
            project_id, "Asset"
        )
        project = projects_service.get_project(project_id)
        self.is_tv_show = projects_service.is_tv_show(project)
        if self.is_tv_show:
            episodes = shots_service.get_episodes_for_project(project_id)
            self.episodes = {
                episode["name"]: episode["id"] for episode in episodes
            }
        self.created_assets = []
        self.task_types_in_project_for_assets = (
            TaskType.query.join(ProjectTaskTypeLink)
            .filter(ProjectTaskTypeLink.project_id == project_id)
            .filter(TaskType.for_entity == "Asset")
        )
        self.task_statuses = {
            status["id"]: [status[n] for n in ("name", "short_name")]
            for status in get_task_statuses()
        }
        self.current_user_id = get_current_user()["id"]
        self.task_types_for_ready_for_map = {
            task_type.name: str(task_type.id)
            for task_type in TaskType.query.join(ProjectTaskTypeLink)
            .filter(ProjectTaskTypeLink.project_id == project_id)
            .filter(TaskType.for_entity == "Shot")
            .all()
        }

    def get_tasks_update(self, row):
        tasks_update = []
        for task_type in self.task_types_in_project_for_assets:
            task_status_name = row.get(task_type.name, None)
            task_status_id = None
            if task_status_name is not None:
                for status_id, status_names in self.task_statuses.items():
                    if task_status_name in status_names:
                        task_status_id = status_id
                        break
                if task_status_id is None:
                    raise RowException(
                        "Task status not found for %s" % task_status_name
                    )

            task_comment_text = row.get("%s comment" % task_type.name, None)

            if task_status_id is not None or task_comment_text is not None:
                tasks_update.append(
                    {
                        "task_type_id": str(task_type.id),
                        "task_status_id": task_status_id,
                        "comment": task_comment_text,
                    }
                )

        return tasks_update

    def create_and_update_tasks(
        self, tasks_update, entity, asset_created=False
    ):
        if tasks_update:
            if asset_created:
                tasks_map = {
                    str(task_type.id): create_task(
                        task_type.serialize(), entity.serialize()
                    )
                    for task_type in self.task_types_in_project_for_assets
                }
            else:
                tasks_map = {
                    task["task_type_id"]: task
                    for task in get_tasks_for_asset(str(entity.id))
                }

            for task_update in tasks_update:
                if task_update["task_type_id"] not in tasks_map:
                    tasks_map[task_update["task_type_id"]] = create_task(
                        get_task_type(task_update["task_type_id"]),
                        entity.serialize(),
                    )
                task = tasks_map[task_update["task_type_id"]]
                if (
                    task_update["comment"] is not None
                    or task_update["task_status_id"] != task["task_status_id"]
                ):
                    create_comment(
                        self.current_user_id,
                        task["id"],
                        task_update["task_status_id"]
                        or task["task_status_id"],
                        task_update["comment"] or "",
                        [],
                        {},
                        "",
                    )
        elif asset_created:
            self.created_assets.append(entity.serialize())

    def import_row(self, row, project_id):
        asset_name = row["Name"]
        entity_type_name = row["Type"]
        episode_name = row.get("Episode", None)
        episode_id = None

        if self.is_tv_show:
            if episode_name not in [None, "MP"] + list(self.episodes.keys()):
                self.episodes[
                    episode_name
                ] = shots_service.get_or_create_episode(
                    project_id, episode_name
                )[
                    "id"
                ]
            episode_id = self.episodes.get(episode_name, None)
        elif episode_name is not None:
            raise RowException(
                "An episode column is present for a production that isn't a TV Show"
            )

        self.add_to_cache_if_absent(
            self.entity_types,
            assets_service.get_or_create_asset_type,
            entity_type_name,
        )
        entity_type_id = self.get_id_from_cache(
            self.entity_types, entity_type_name
        )

        asset_values = {
            "name": asset_name,
            "project_id": project_id,
            "entity_type_id": entity_type_id,
            "source_id": episode_id,
        }

        entity = Entity.get_by(**asset_values)

        asset_new_values = {}

        description = row.get("Description", None)
        if description is not None:
            asset_new_values["description"] = description

        if entity is None:
            asset_new_values["data"] = {}
        else:
            asset_new_values["data"] = entity.data or {}

        for name, field_name in self.descriptor_fields.items():
            if name in row:
                asset_new_values["data"][field_name] = row[name]

        ready_for = row.get("Ready for", None)
        if ready_for is not None:
            try:
                asset_new_values[
                    "ready_for"
                ] = self.task_types_for_ready_for_map[ready_for]
            except KeyError:
                raise RowException("Task type not found for %s" % ready_for)

        tasks_update = self.get_tasks_update(row)

        if entity is None:
            entity = Entity.create(**{**asset_values, **asset_new_values})
            events.emit(
                "asset:new",
                {"asset_id": str(entity.id), "episode_id": episode_id},
                project_id=project_id,
            )

            self.create_and_update_tasks(
                tasks_update, entity, asset_created=True
            )

        elif self.is_update:
            entity.update(asset_new_values)
            events.emit(
                "asset:update",
                {"asset_id": str(entity.id), "episode_id": episode_id},
                project_id=project_id,
            )

            self.create_and_update_tasks(
                tasks_update, entity, asset_created=False
            )

        return entity.serialize()

    def run_import(self, project_id, file_path):
        entities = super().run_import(project_id, file_path)
        for task_type in self.task_types_in_project_for_assets:
            create_tasks(task_type.serialize(), self.created_assets)
        return entities
