from rest_framework import status


def test_create_payment_success(mocker, user, course):
    mock_service = mocker.patch('payments.services.create_payment_session')
    mock_service.return_value = {
        "payment_id": 1,
        "checkout_url": "https://checkout.stripe.com/...",
        "session_id": "cs_test_..."
    }

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post('/api/payments/create/', {
        'course_id': course.id,
        'amount': 1990.00,
    }, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert mock_service.called
    assert mock_service.call_args[0] == (user, course, 1990.0)


class APIClient:
    pass


def test_create_payment_invalid_amount(mocker, user, course):
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post('/api/payments/create/', {
        'course_id': course.id,
        'amount': -100,  # невалидное значение
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'amount' in response.data['error']



