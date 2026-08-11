import pytest
from unittest.mock import patch
from views import trainee_view


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Fixture que se ejecuta automáticamente antes de cada prueba.
    Garantiza un entorno limpio o simulado.
    """
    yield


# --- PRUEBA 1: Registro Exitoso ---
@patch("templates.trainee_template.display_message")
@patch("templates.trainee_template.get_trainee_input")
@patch("models.trainee_model.register_trainee")
@patch("models.trainee_model.search_by_document")
def test_register_trainee_view_success(
    mock_search, mock_register, mock_get_input, mock_display_msg
):
    """Prueba que un aprendiz se registre exitosamente si no existe previamente."""

    mock_input_data = {
        "tipo_doc": "CC",
        "documento": "12345",
        "nombre": "Juan Perez",
        "ficha": "2671234",
        "programa": "ADSO",
        "email": "juan@sena.edu.co",
    }
    mock_get_input.return_value = mock_input_data

    mock_search.return_value = None

    trainee_view.register_trainee_view()

    mock_search.assert_called_once_with("12345")
    mock_register.assert_called_once_with(mock_input_data)
    mock_display_msg.assert_called_once_with(
        {
            "type": "success",
            "text": "Aprendiz Juan Perez registrado exitosamente con el correo juan@sena.edu.co.",
        }
    )


# --- PRUEBA 2: Registro Duplicado ---
@patch("templates.trainee_template.display_message")
@patch("templates.trainee_template.get_trainee_input")
@patch("models.trainee_model.register_trainee")
@patch("models.trainee_model.search_by_document")
def test_register_trainee_view_duplicate(
    mock_search, mock_register, mock_get_input, mock_display_msg
):
    """Prueba que se muestre error si el documento ya está registrado."""

    mock_input_data = {
        "tipo_doc": "CC",
        "documento": "12345",
        "nombre": "Juan Perez",
        "ficha": "2671234",
        "programa": "ADSO",
        "email": "juan@sena.edu.co",
    }
    mock_get_input.return_value = mock_input_data

    mock_search.return_value = mock_input_data

    trainee_view.register_trainee_view()

    mock_search.assert_called_once_with("12345")
    mock_register.assert_not_called()
    mock_display_msg.assert_called_once_with(
        {
            "type": "error",
            "text": "Ya existe un aprendiz registrado con este número de documento.",
        }
    )


# --- PRUEBA 3: Listado de Aprendices ---
@patch("templates.trainee_template.display_trainees_list")
@patch("models.trainee_model.get_all")
def test_list_view(mock_get_all, mock_display_list):
    """Prueba que list_view obtenga todos los aprendices y los envíe a la plantilla."""

    mock_trainees = [
        {"documento": "123", "nombre": "Ana"},
        {"documento": "456", "nombre": "Carlos"},
    ]

    mock_get_all.return_value = mock_trainees

    trainee_view.list_view()

    mock_get_all.assert_called_once()

    mock_display_list.assert_called_once_with(
        mock_trainees,
        "Todos los Aprendices Registrados",
    )