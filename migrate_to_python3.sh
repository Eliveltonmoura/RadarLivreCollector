#!/bin/bash

echo "=== Migrando RadarLivreCollector para Python 3 ==="

# Backup do projeto original
echo "Criando backup..."
cp -r . ../RadarLivreCollector_backup

# Converter todos os arquivos Python
echo "Convertendo arquivos Python..."
find . -name "*.py" -exec 2to3 -w {} \;

# Atualizar shebangs
echo "Atualizando shebangs..."
find . -name "*.py" -exec sed -i '1s|^#!/usr/bin/python$|#!/usr/bin/python3|' {} \;

# Atualizar scripts shell
echo "Atualizando scripts shell..."
sed -i 's/\bpython\b/python3/g' INSTALL.sh
sed -i 's/\bpip\b/pip3/g' INSTALL.sh
sed -i 's/python-dev/python3-dev/g' INSTALL.sh

sed -i 's/\bpython\b/python3/g' CONFIGURE.sh
sed -i 's/\bpip\b/pip3/g' CONFIGURE.sh

if [ -f "start_receptor" ]; then
    sed -i 's/\bpython\b/python3/g' start_receptor
fi

echo "=== Migração concluída! ==="
echo "Verifique os arquivos e teste a instalação."