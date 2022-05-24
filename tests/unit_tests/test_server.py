import server

server.clubs = [
    {
        "name":"TOP-official",
        "email":"josh@twentyonepilots.com",
        "points":"15"
    },
    {
        "name":"TOP-France",
        "email": "tyler@twentyonepilots.fr",
        "points":"4"
    }
]

server.competitions = [
	{
		"name": "Parissun",
		"date": "2020-04-25 9:00:00",
		"numberOfPlaces": "21"
	},
	{
		"name": "Backker",
		"date": "2025-01-10 14:00:00",
		"numberOfPlaces": "13"
	},
	{
		"name": "Musclor",
		"date": "2025-02-24 11:30:00",
		"numberOfPlaces": "5"
	}
]


def test_unknown_email_adress(client):
	response = client.post('/showSummary', data={"email": "unknown@fakeadress.com"})
	assert response.status_code == 200
	assert "Unknown email adress !" in response.data.decode()
	

def test_correct_email_adress(client):
	email = "josh@twentyonepilots.com"
	response = client.post('/showSummary', data={"email": email})
	assert response.status_code == 200
	assert ("Welcome, " + email) in response.data.decode()


def test_oudated_comp(client):
	response = client.get('/book/Parissun/TOP-official')
	assert "Something went wrong-please try again" in response.data.decode()
	assert response.status_code == 200


def test_should_status_code_ok(client):
	response = client.get('/')
	assert response.status_code == 200


def test_clubs_table_points(client):
	response = client.get('/clubsboard')
	assert response.status_code == 200
	assert server.clubs[0]["name"] in response.data.decode()
	assert server.clubs[1]["points"] in response.data.decode()


def test_logout(client):
	response = client.get('/logout')
	assert response.status_code == 302
