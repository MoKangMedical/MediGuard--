#!/bin/bash
echo "🛡️ MediGuard 医保智盾"
echo "====================="
python3 -m py_compile src/engine.py && echo "✅ engine.py"
mkdir -p output data
echo "✅ 部署完成"
