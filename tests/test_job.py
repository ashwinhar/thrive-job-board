"""Tests files in the /job_boards/ directory"""
import pytest
from job_boards.job import Job

### Testing Job ###

job = Job(company="Company", position="Position", location="Location")
job.set_id()
job_id = job.id


def test_init():
    """" Tests basic initialization of a Job instance"""
    assert job.company == "Company" and job.position == "Position" and job.location == "Location"


def test_to_string():
    """Tests magic __str__ method"""
    assert str(
        job) == f"Job(id: {job_id}, company: Company, position: Position, location: Location)"


def test_company_setter():
    """Tests setting company attribute"""
    with pytest.raises(TypeError) as message:
        job.company = 3  # type: ignore

    assert "must be a string" in str(message)


def test_position_setter():
    """Tests setting position attribute"""
    with pytest.raises(TypeError) as message:
        job.position = 3

    assert "must be a string" in str(message)


def test_location_setter():
    """Tests setting location attribute"""
    with pytest.raises(TypeError) as message:
        job.location = 3

    assert "must be a string" in str(message)


def test_to_dict():
    """Tests to_dict() method functions correctly"""

    job_dict = job.to_dict()

    assert job_dict.get("_company") == "Company" and job_dict.get(
        "_position") == "Position" and job_dict.get("_location") == "Location"


def test_clean_strings():
    """Tests if clean_strings() functions correctly"""

    test_job = Job(company="    Company   ",
                   position="\n   Position   ", location="Location")

    test_job.clean_strings()

    assert test_job.company == "Company" and test_job.position == "Position"


def test_load_from_dict():
    """Tests load from dict"""
    job_dict = job.to_dict()

    new_job = Job.load_from_dict(job_dict)

    assert new_job.company == "Company" and new_job.position == "Position" \
        and new_job.location == "Location"
