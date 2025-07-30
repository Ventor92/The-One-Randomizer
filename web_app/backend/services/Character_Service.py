from ..models.chatRecord import RecordBase
from ..models.TheNewOrigin.Item import TNOItem_ORM, TNOItemDTO
from ..models.TheNewOrigin.Character import TNO_Character_ORM, TNO_Character_DTO, TNO_AttributesSheet_ORM, TNO_AttributesSheet_DTO

from ..database.Repository_Controller import RepositoryController
from ..database.Repository_Service import RepositoryService
from sqlmodel import Session
from collections.abc import Sequence

class CharacterRepository(RepositoryService[TNO_Character_ORM]):
    model = TNO_Character_ORM

class AttributesRepository(RepositoryService[TNO_AttributesSheet_ORM]):
    model = TNO_AttributesSheet_ORM

class Character_Service:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("This class cannot be instantiated. Use static methods only.")
    
    @staticmethod
    def add_item(item: TNOItemDTO) -> TNOItemDTO:
        """
        Adds an item to the character's inventory.
        :param item: TNOItemDTO object to be added.
        :return: The added TNOItemDTO object.
        """

        orm = TNOItem_ORM(**item.model_dump())

        engine = RepositoryController.getEngine()
        with Session(engine) as session:
            RepositoryService.add(session, orm)
        dto = TNOItemDTO.model_validate(orm)
        return dto
    
    @staticmethod
    def get_items(character_id: int) -> Sequence[TNOItemDTO]:
        """
        Retrieves the items of a character.
        :param character_id: ID of the character.
        :return: A list of TNOItemDTO objects.
        """
        orm: TNO_Character_ORM | None = None
        engine = RepositoryController.getEngine()

        with Session(engine) as session:
            orm = CharacterRepository.get(session, character_id)

            # return [TNOItemDTO(id=999, name="Test Item", isCursed=False, owner_id=0)]
            
            if not orm:
                return []
            else: 
                orm_items = orm.items
                items = [TNOItemDTO.model_validate(item) for item in orm_items]
                return items
            
    @staticmethod
    def createCharacter(dto: TNO_Character_DTO) -> TNO_Character_DTO:
        charORM = TNO_Character_ORM(name=dto.name, user_id=dto.user_id)

        skillsORM = TNO_AttributesSheet_ORM(character=charORM)

        engine = RepositoryController.getEngine()
        with Session(engine) as session:
            charORM = CharacterRepository.add(session, charORM)
            # CharacterRepository.add(session, charORM)

        dto = TNO_Character_DTO.model_validate(charORM)

        return dto
    
    @staticmethod
    def updateCharacterAttribute(dto: TNO_AttributesSheet_DTO, character_id: int) -> TNO_AttributesSheet_DTO:
        
        charORM: TNO_Character_ORM | None = None
        engine = RepositoryController.getEngine()

        with Session(engine) as session:
            charORM = CharacterRepository.get(session, character_id)
            if charORM is not None:
                charORM.updateAttrByDTO(dto)
                charORM = CharacterRepository.update(session, charORM)
                attORM = charORM.getAttributesSheet()
                dto = TNO_AttributesSheet_DTO.model_validate(attORM)
            else:
                pass

        return dto
    
    @staticmethod
    def getCharacterAttribute(character_id: int) -> TNO_AttributesSheet_DTO:
        
        charORM: TNO_Character_ORM | None = None
        engine = RepositoryController.getEngine()

        dto: TNO_AttributesSheet_DTO = TNO_AttributesSheet_DTO(id = None)

        with Session(engine) as session:
            charORM = CharacterRepository.get(session, character_id)
            if charORM is not None:
                attrORM = charORM.getAttributesSheet()
                dto = TNO_AttributesSheet_DTO.model_validate(attrORM)
            else:
                pass

        return dto
            
