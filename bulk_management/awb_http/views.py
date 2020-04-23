from anyblok_pyramid import current_blok
from pyramid.view import view_config, view_defaults
from sqlalchemy.types import Boolean


@view_defaults(installed_blok=current_blok())
class ContainerViews:
    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

    @view_config(route_name="container_list", renderer="json")
    def route_containers(self):
        Wms = self.registry.Wms
        return (
            Wms.PhysObj.query()
            .filter(Wms.PhysObj.Type.behaviours["container"].astext.cast(Boolean))
            .order_by(Wms.PhysObj.code)
            .all()
            .to_dict()
        )

    @view_config(route_name="container_type", renderer="json")
    def route_container_type(self):
        Wms = self.registry.Wms
        return Wms.PhysObj.Type.query().get(self.request.matchdict["id"]).to_dict()
