import pytest
from models import trainee_model


@pytest.fixture(autouse=True)
def clean_state(monkeypatch, tmp_path):
    """Deja el modelo en un estado limpio para cada prueba."""
    monkeypatch.setattr(trainee_model, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(trainee_model, "DATA_FILE", tmp_path / "data" / "trainees.json")
    monkeypatch.setattr(trainee_model, "CSV_FILE", tmp_path / "data" / "trainees.csv")
    trainee_model.trainees = []
    trainee_model.ensure_data_file_exists()
    yield
    trainee_model.trainees = []


def test_load_from_json_reads_saved_data():
    """Prueba que se carguen los aprendices guardados en el archivo JSON."""
    trainee_model.trainees = [
        {
            "tipo_doc": "CC",
            "documento": "12345",
            "nombre": "Juan Perez",
            "ficha": "2671234",
            "programa": "ADSO",
            "email": "juan@sena.edu.co",
        }
    ]
    trainee_model.save_to_json()

    trainee_model.trainees = []
    loaded = trainee_model.load_from_json()

    assert loaded[0]["documento"] == "12345"
    assert loaded[0]["nombre"] == "Juan Perez"


def test_register_trainee_success():
    """Prueba que un aprendiz nuevo se registre correctamente."""
    new_trainee = {
        "tipo_doc": "CC",
        "documento": "12345",
        "nombre": "Juan Perez",
        "ficha": "2671234",
        "programa": "ADSO",
        "email": "juan@sena.edu.co",
    }

    result = trainee_model.register_trainee(new_trainee)

    assert result is True
    assert trainee_model.search_by_document("12345") == new_trainee
    assert len(trainee_model.trainees) == 1


def test_register_trainee_duplicate_returns_false():
    """Prueba que no se registren documentos duplicados."""
    existing_trainee = {
        "tipo_doc": "CC",
        "documento": "12345",
        "nombre": "Juan Perez",
        "ficha": "2671234",
        "programa": "ADSO",
        "email": "juan@sena.edu.co",
    }
    trainee_model.trainees = [existing_trainee]

    result = trainee_model.register_trainee(existing_trainee)

    assert result is False
    assert len(trainee_model.trainees) == 1


def test_update_trainee_success():
    """Prueba que se actualicen los datos de un aprendiz existente."""
    trainee_model.trainees = [
        {
            "tipo_doc": "CC",
            "documento": "12345",
            "nombre": "Juan Perez",
            "ficha": "2671234",
            "programa": "ADSO",
            "email": "juan@sena.edu.co",
        }
    ]

    result = trainee_model.update_trainee(
        "12345",
        {"nombre": "Juan Actualizado", "email": "juan.actualizado@sena.edu.co"},
    )

    assert result is True
    assert trainee_model.search_by_document("12345")["nombre"] == "Juan Actualizado"
    assert trainee_model.search_by_document("12345")["email"] == "juan.actualizado@sena.edu.co"


def test_delete_trainee_success():
    """Prueba que se elimine correctamente un aprendiz."""
    trainee_model.trainees = [
        {
            "tipo_doc": "CC",
            "documento": "12345",
            "nombre": "Juan Perez",
            "ficha": "2671234",
            "programa": "ADSO",
            "email": "juan@sena.edu.co",
        },
        {
            "tipo_doc": "TI",
            "documento": "67890",
            "nombre": "Ana Gomez",
            "ficha": "9876543",
            "programa": "ADSI",
            "email": "ana@sena.edu.co",
        },
    ]

    result = trainee_model.delete_trainee("12345")

    assert result is True
    assert trainee_model.search_by_document("12345") is None
    assert len(trainee_model.trainees) == 1


def test_search_by_name_or_group_filters_results():
    """Prueba que la búsqueda filtre por nombre o ficha."""
    trainee_model.trainees = [
        {
            "tipo_doc": "CC",
            "documento": "12345",
            "nombre": "Juan Perez",
            "ficha": "2671234",
            "programa": "ADSO",
            "email": "juan@sena.edu.co",
        },
        {
            "tipo_doc": "TI",
            "documento": "67890",
            "nombre": "Ana Gomez",
            "ficha": "9876543",
            "programa": "ADSI",
            "email": "ana@sena.edu.co",
        },
    ]

    results = trainee_model.search_by_name_or_group("267")

    assert len(results) == 1
    assert results[0]["documento"] == "12345"
