"""Download public kernel v2 outputs without logging signed URLs."""

import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    from kaggle import api
    from kagglesdk.kernels.types.kernels_api_service import ApiGetKernelRequest, ApiListKernelSessionOutputRequest

    ref = "muelsyse111/kaggriculture-exp006-independent-baseline-audit"
    expected = {"cloud-runtime.json", "cloud-tests.xml", "runtime-verification.json", "submission.tar.gz"}
    outputs = {}
    with api.build_kaggle_client() as client:
        service = client.kernels.kernels_api_client
        identity = ApiGetKernelRequest()
        identity.user_name, identity.kernel_slug = ref.split("/")
        def check():
            metadata = service.get_kernel(identity).metadata
            if metadata.is_private or metadata.current_version_number != 2:
                raise ValueError("Public kernel version changed")
            if api.kernels_status(ref).to_dict()["status"] != "COMPLETE":
                raise ValueError("Kernel is not complete")
        check()
        request = ApiListKernelSessionOutputRequest()
        request.user_name, request.kernel_slug = ref.split("/")
        while True:
            response = service.list_kernel_session_output(request)
            for item in response.files or []:
                if item.file_name not in expected:
                    continue
                if item.file_name in outputs:
                    raise ValueError("Duplicate output")
                result = subprocess.run(["/usr/bin/curl", "--fail", "--location", "--silent",
                                         "--show-error", "--retry", "2", "--max-time", "60", item.url],
                                        capture_output=True, timeout=200)
                if result.returncode:
                    raise RuntimeError("Output transfer failed for " + item.file_name
                                       + "; curl exit " + str(result.returncode))
                outputs[item.file_name] = result.stdout
            if not response.next_page_token:
                break
            request.page_token = response.next_page_token
        check()
    if outputs.keys() != expected:
        raise ValueError("Missing expected output files")
    for name in ("cloud-runtime.json", "runtime-verification.json"):
        json.loads(outputs[name])
    folder = ROOT / "kaggle_notebooks/exp006-validation/output"
    folder.mkdir(parents=True, exist_ok=True)
    for name, payload in outputs.items():
        (folder / name).write_bytes(payload)
    print(json.dumps({"kernel_ref": ref, "kernel_version": 2,
                      "files": {name: len(payload) for name, payload in outputs.items()}}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("DOWNLOAD_FAILED:", type(error).__name__, "Raw diagnostics suppressed; no submission performed.")
        raise SystemExit(1)
