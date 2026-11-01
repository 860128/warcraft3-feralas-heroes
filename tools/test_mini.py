import subprocess, time

test_dir = "test_factory_mini"
import os, shutil
if os.path.exists(test_dir): shutil.rmtree(test_dir)
os.makedirs(f"{test_dir}/table", exist_ok=True)
shutil.copy("factory_tpl/table/ability.ini", f"{test_dir}/table/ability.ini")
shutil.copy("factory_tpl/table/unit.ini", f"{test_dir}/table/unit.ini")

t0 = time.time()
p = subprocess.run(["tools/w3x2lni/w2l.exe", "obj", test_dir, "test_mini.w3x"], capture_output=True, text=True)
print("Time:", time.time() - t0)
print("RC:", p.returncode)
print("STDOUT:", p.stdout)
print("STDERR:", p.stderr)
