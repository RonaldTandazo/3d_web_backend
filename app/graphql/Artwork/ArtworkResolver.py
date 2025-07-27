import strawberry
from app.config.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from strawberry.exceptions import GraphQLError
from app.utils.helpers import Helpers
import asyncio
from app.graphql.Artwork.ArtworkInputs import StoreArtworkInput
from app.graphql.Artwork.ArtworkPayloads import ArtworkPayload, ArtworkDetailsPayload, ArtworkFormData
from app.services.Artwork.ArtworkService import ArtworkService
from app.services.Artwork.ArtworkOwnerService import ArtworkOwnerService
from app.services.Artwork.ArtworkThumbnailService import ArtworkThumbnailService
from app.services.Artwork.ArtworkCategoryService import ArtworkCategoryService
from app.services.Artwork.ArtworkSoftwareService import ArtworkSoftwareService
from app.services.Artwork.ArtworkTopicService import ArtworkTopicService
from app.services.General.CategoryService import CategoryService
from app.services.General.TopicService import TopicService
from app.services.General.SoftwareService import SoftwareService
from app.services.General.PublishingService import PublishingService
from app.graphql.Category.CategoryPayloads import CategoryPayload
from app.graphql.Topic.TopicPayloads import TopicPayload
from app.graphql.Software.SoftwarePayloads import SoftwarePayload
from app.graphql.Publishing.PublishingPayloads import PublishingPayload
from typing import AsyncGenerator

@strawberry.type
class NewArtworkPayload:
    artwork: ArtworkPayload

artwork_queue: asyncio.Queue[NewArtworkPayload] = asyncio.Queue()

async def artwork_creation_generator():
    while True:
        new_artwork_payload = await artwork_queue.get()
        yield new_artwork_payload

@strawberry.type
class ArtworkMutation:
    @strawberry.mutation
    async def storeArtwork(self, info, artworkData: StoreArtworkInput) -> ArtworkPayload:
        db = info.context["db"]
        current_user = info.context["current_user"]
        request = info.context["request"]

        awk_service = ArtworkService(db)
        awk_owner_service = ArtworkOwnerService(db)
        awk_thmb_service = ArtworkThumbnailService(db)
        awk_ctg_service = ArtworkCategoryService(db)
        awk_sfw_service = ArtworkSoftwareService(db)
        awk_tpc_service = ArtworkTopicService(db)
        
        ip = await Helpers.getIp(request)
        terminal = await Helpers.getRequestAgents(request)
        filename = None
        try:
            store_artwork = await awk_service.store(
                artworkData.title,
                artworkData.description,
                artworkData.matureContent,
                ip,
                terminal,
                artworkData.publishing
            )

            if not store_artwork.get("ok", False):
                raise GraphQLError(message=store_artwork['error'], extensions={"code": "BAD_USER_INPUT"})

            artwork = store_artwork.get("data")

            store_artwork_owner = await awk_owner_service.store(
                artwork.artwork_id,
                current_user.userId,
                ip,
                terminal
            )

            if not store_artwork_owner.get("ok", False):
                raise GraphQLError(message=store_artwork_owner['error'], extensions={"code": "BAD_USER_INPUT"})

            if artworkData.categories and len(artworkData.categories) > 0:
                store_artwork_categories = await awk_ctg_service.store(
                    artwork.artwork_id,
                    artworkData.categories,
                    ip,
                    terminal
                )

                if not store_artwork_categories.get("ok", False):
                    raise GraphQLError(message=store_artwork_categories['error'], extensions={"code": "BAD_USER_INPUT"})
                
            if artworkData.softwares and len(artworkData.softwares) > 0:
                store_artwork_softwares = await awk_sfw_service.store(
                    artwork.artwork_id,
                    artworkData.softwares,
                    ip,
                    terminal
                )

                if not store_artwork_softwares.get("ok", False):
                    raise GraphQLError(message=store_artwork_softwares['error'], extensions={"code": "BAD_USER_INPUT"})
                
            if artworkData.topics and len(artworkData.topics) > 0:
                store_artwork_topics = await awk_tpc_service.store(
                    artwork.artwork_id,
                    artworkData.topics,
                    ip,
                    terminal
                )

                if not store_artwork_topics.get("ok", False):
                    raise GraphQLError(message=store_artwork_topics['error'], extensions={"code": "BAD_USER_INPUT"})
                
            if artworkData.thumbnail and artworkData.thumbnail != '':
                thumbnail_name = artworkData.title+" Thumbnail"
                filename = await Helpers.generateRandomFilename(".jpeg")
                thumbnail_store = await Helpers.decodedAndSaveImg(filename, artworkData.thumbnail, "thumbnail")
                if not thumbnail_store.get("ok", False):
                    raise GraphQLError(message=thumbnail_store['error'], extensions={"code": "INTERNAL_SERVER_ERROR"})

                store_artwork_thumbnail = await awk_thmb_service.store(
                    artwork.artwork_id, 
                    filename, 
                    thumbnail_name,
                    ip,
                    terminal
                )

                if not store_artwork_thumbnail.get("ok", False):
                    raise GraphQLError(message=store_artwork_thumbnail['error'], extensions={"code": "INTERNAL_SERVER_ERROR"})

            await artwork_queue.put(NewArtworkPayload(artwork=ArtworkPayload(
                artworkId=artwork.artwork_id,
                title=artwork.title,
                thumbnail=filename,
                publishingId=artworkData.publishing,
                owner=current_user.userId,
                createdAt=artwork.created_at
            )))

            return ArtworkPayload(artworkId=artwork.artwork_id, title=artwork.title, thumbnail=filename, publishingId=artworkData.publishing, owner=current_user.userId, createdAt=artwork.created_at)

        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "E-mail already in used"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
        
@strawberry.type
class ArtworkQuery:
    @strawberry.field
    async def getUserArtworks(self, info) -> list[ArtworkPayload]:
        db = info.context["db"]
        current_user = info.context["current_user"]
        awk_owner_service = ArtworkOwnerService(db)
        try:
            artworks = await awk_owner_service.getUserArtworks(current_user.userId)

            if not artworks.get("ok", False):
                raise GraphQLError(message=artworks['error'], extensions={"code": "NOT_FOUND"})
            
            artworks = artworks.get("data")

            return [ArtworkPayload(artworkId=artwork['artwork_id'], title=artwork['title'], thumbnail=artwork['thumbnail'], publishingId=artwork['publishingId'], owner=artwork['owner'], createdAt=artwork['createdAt']) for artwork in artworks]
        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "E-mail already in used"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
        
    @strawberry.field
    async def getArtworkDetails(self, info, artworkId: int) -> ArtworkDetailsPayload:
        db = info.context["db"]
        awk_service = ArtworkService(db)
        try:
            artwork = await awk_service.getArtworkDetails(artworkId)

            if not artwork.get("ok", False):
                raise GraphQLError(message=artwork['error'], extensions={"code": "NOT_FOUND"})
            
            artwork = artwork.get("data")

            return ArtworkDetailsPayload(
                artworkId=artwork['artwork_id'], 
                title=artwork['title'], 
                description=artwork['description'], 
                matureContent=artwork['mature_content'], 
                categories=artwork['categories'], 
                topics=artwork['topics'], 
                softwares=artwork['softwares'],
                publishingId=artwork['publishing_id'], 
                thumbnail=artwork['thumbnail'], 
                createdAt=artwork['created_at']
            )
        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "E-mail already in used"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
        
    @strawberry.field
    async def getArtworkFormData(self, info) ->ArtworkFormData:
        db = info.context["db"]
        ctg_service = CategoryService(db)
        tpc_service = TopicService(db)
        sft_service = SoftwareService(db)
        pbl_service = PublishingService(db)
        try:
            categories = await ctg_service.getCategories()
            categories = categories.get("data") if categories.get("ok") else []
            categories = [
                CategoryPayload(categoryId=item.category_id, name=item.name)
                for item in categories
            ]

            topics = await tpc_service.getTopics()
            topics = topics.get("data") if topics.get("ok") else []
            topics = [
                TopicPayload(topicId=item.topic_id, name=item.name)
                for item in topics
            ]

            softwares = await sft_service.getSoftware()
            softwares = softwares.get("data") if softwares.get("ok") else []
            softwares = [
                SoftwarePayload(softwareId=item.software_id, name=item.name)
                for item in softwares
            ]

            publishing = await pbl_service.getPublishing()
            publishing = publishing.get("data") if publishing.get("ok") else []
            publishing = [
                PublishingPayload(publishingId=item.publishing_id, name=item.name)
                for item in publishing
            ]

            return ArtworkFormData(categories=categories, topics=topics, softwares=softwares, publishing=publishing)
        except GraphQLError as e:
            logger.error(e.message)
            raise e

        except Exception as e:
            error_mapping = {
                IntegrityError: ("BAD_USER_INPUT", "E-mail already in used"),
                SQLAlchemyError: ("INTERNAL_SERVER_ERROR", "Error interno del servidor"),
                ValueError: ("BAD_USER_INPUT", "Datos inválidos"),
                PermissionError: ("FORBIDDEN", "Permiso denegado"),
                FileNotFoundError: ("NOT_FOUND", "Archivo no encontrado"),
                ConnectionError: ("TOO_MANY_REQUESTS", "Demasiadas solicitudes"),
            }

            extension_code, error_message = error_mapping.get(type(e), ("INTERNAL_SERVER_ERROR", "Error desconocido"))
            logger.error(error_message)
            raise GraphQLError(message=error_message, extensions={"code": extension_code})
        
@strawberry.type
class ArtworkSubscription:
    @strawberry.subscription
    async def newArtwork(self) -> AsyncGenerator[NewArtworkPayload, None]:
        async for artwork_payload in artwork_creation_generator():
            yield artwork_payload