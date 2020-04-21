import pytest

LOC_INCOMING = "incoming"
LOC_WAREHOUSE = "warehouse"


@pytest.fixture(scope="function")
def location_type(rollback_registry):
    Wms = rollback_registry.Wms
    return Wms.PhysObj.Type.insert(code="LOCATION", behaviours=dict(container=True))


@pytest.fixture(scope="function")
def root_container(rollback_registry, location_type):
    Wms = rollback_registry.Wms
    return Wms.create_root_container(location_type, code=LOC_WAREHOUSE)


@pytest.fixture(scope="function")
def incoming_container(rollback_registry, location_type, root_container):
    Wms = rollback_registry.Wms
    return Wms.Operation.Apparition.create(
        state="done",
        location=root_container,
        quantity=1,
        goods_type=location_type,
        goods_code=LOC_INCOMING,
    )


@pytest.mark.usefixtures("rollback_registry")
class TestPyramidExampleViews:
    """ Test pyramid routes with PyramidBlokTestCase"""

    def test_get_containers(self, webserver, root_container, incoming_container):
        """Test pyramid Example get route /"""
        response = webserver.get("/api/containers")
        assert response.status == "200 OK"
        assert response.json[0]["code"] == LOC_INCOMING
        assert response.json[1]["code"] == LOC_WAREHOUSE
