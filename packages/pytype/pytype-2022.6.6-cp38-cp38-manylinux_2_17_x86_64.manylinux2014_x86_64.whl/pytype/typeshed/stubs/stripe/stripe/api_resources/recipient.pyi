from stripe.api_resources.abstract import (
    CreateableAPIResource as CreateableAPIResource,
    DeletableAPIResource as DeletableAPIResource,
    ListableAPIResource as ListableAPIResource,
    UpdateableAPIResource as UpdateableAPIResource,
)

class Recipient(CreateableAPIResource, DeletableAPIResource, ListableAPIResource, UpdateableAPIResource):
    OBJECT_NAME: str
