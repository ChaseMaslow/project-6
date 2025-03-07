from mongoengine import *



class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        distance: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    
    distance = FloatField(required=True)
    location = StringField(null=True)
    open_time = DateTimeField(required=True)
    close_time = DateTimeField(required=True)
    
    pass


class Brevet(Document):
    """
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    
    length = FloatField(min_value=0, required=True)
    start_time = DateTimeField(required=True)
    checkpoints = ListField(EmbeddedDocumentField(Checkpoint), required=True)
    
    pass
