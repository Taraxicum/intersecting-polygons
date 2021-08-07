from polygon_intersection_generator import PolygonIntersectionGenerator

def test_is_outside_polygon():
    print("Testing is_outside_polygon")
    pig = PolygonIntersectionGenerator(13)
    assert pig.is_outside_polygon([[]])
    assert pig.is_outside_polygon([[1, 2, 3, 4, 5, 6]])
    assert pig.is_outside_polygon([[1, 2, 3, 4, 5, 6], [2, 5, 6, 7, 10, 11]])
    assert not pig.is_outside_polygon([[1, 2, 3, 4, 5], [2, 5, 6, 7, 10, 11]])
    assert pig.is_outside_polygon([[1, 2, 3, 4, 5], [2, 5, 6, 7, 10]])

test_is_outside_polygon()
