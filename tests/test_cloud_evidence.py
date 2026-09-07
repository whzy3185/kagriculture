import pytest

from scripts.verify_cloud_evidence import test_count as junit_count


def test_junit_counts_actual_cases(tmp_path):
    path = tmp_path / "tests.xml"
    path.write_text('<testsuites><testsuite tests="1"><testcase name="ok"/></testsuite></testsuites>')
    assert junit_count(path, 1) == 1


@pytest.mark.parametrize("field", ["errors", "failures", "skipped"])
def test_junit_rejects_nonpassing_cases(tmp_path, field):
    path = tmp_path / "tests.xml"
    path.write_text(f'<testsuite tests="1" {field}="1"><testcase name="bad"/></testsuite>')
    with pytest.raises(ValueError):
        junit_count(path, 1)


def test_junit_rejects_inflated_counts(tmp_path):
    path = tmp_path / "tests.xml"
    path.write_text('<testsuite tests="2"><testcase name="only-one"/></testsuite>')
    with pytest.raises(ValueError):
        junit_count(path, 1)
