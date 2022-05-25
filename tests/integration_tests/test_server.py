from tests.unit_tests.test_server import server
from tests.unit_tests.conftest import client



number_point_for_a_place = 1


def test_futur_comp(client):
	comp = server.competitions[1]
	response = client.get('/book/'+comp['name']+'/TOP-official')
	assert "Places available: " + comp["numberOfPlaces"] in response.data.decode()
	assert response.status_code == 200


def test_purchase_not_enough_point(client):
	comp = server.competitions[1]
	club = server.clubs[1]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 6
		})
	assert "You don&#39;t have enough points" in response.data.decode()
	assert response.status_code == 200


def test_purchase_max_places(client):
	comp = server.competitions[1]
	club = server.clubs[0]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 13
		})
	assert "You can only take a maximum of 12 places" in response.data.decode()
	assert response.status_code == 200


def test_purchase_max_places_available(client):
	comp = server.competitions[2]
	club = server.clubs[0]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 7
		})
	assert "There is not enough places available for this competition." in response.data.decode()
	assert response.status_code == 200


def test_purchase_places(client):
	comp = server.competitions[1]
	club = server.clubs[0]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 3
		})
	assert "Great-booking complete! Number of places purchased: 3" in response.data.decode()
	assert club["points"] == 15-3*number_point_for_a_place
	assert comp["numberOfPlaces"] == 13-3
	assert club[comp['name']] == 3
	assert response.status_code == 200
