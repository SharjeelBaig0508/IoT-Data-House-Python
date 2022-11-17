from mongoengine import Document, QuerySet


def get_single_record(collection: Document, db_filter: dict) -> Document:
    return collection.objects(**db_filter).first()

def get_records(collection: Document, db_filter: dict) -> QuerySet:
    return collection.objects(**db_filter)
