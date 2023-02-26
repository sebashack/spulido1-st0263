BUILD_DIR:=${CURDIR}/_build
VENV_DIR:=${CURDIR}/.env
PYBIN:=${CURDIR}/.env/bin/python

.PHONY: set-py-venv
set-py-venv:
	rm -rf ${VENV_DIR}
	python3 -m venv ${VENV_DIR}
	${PYBIN} -m pip install -U pip wheel setuptools

.PHONY: set-py-venv-with-deps
set-py-venv-with-deps: set-py-venv
	${VENV_DIR}/bin/pip install -r requirements.txt

.PHONY: rabbit-setup
rabbit-setup:
	${PYBIN} ${CURDIR}/mom-setup

.PHONY: run-gateway
run-gateway:
	cd ${CURDIR}/gateway && ${PYBIN} src/__api__.py config.json

.PHONY: run-m1
run-m1:
	cd ${CURDIR}/micro1-grpc && ${PYBIN} src config.json

.PHONY: run-m2
run-m2:
	cd ${CURDIR}/micro2-mom && ${PYBIN} src config.json

.PHONY: build-proto
build-proto:
	rm -rf ${BUILD_DIR}/proto_grpc
	mkdir -p ${BUILD_DIR}/proto_grpc
	${PYBIN} -m grpc_tools.protoc -Iprotos --python_out=${BUILD_DIR}/proto_grpc --pyi_out=${BUILD_DIR}/proto_grpc --grpc_python_out=${BUILD_DIR}/proto_grpc protos/file_service.proto
	rm -rf ${CURDIR}/gateway/src/*_pb2*
	rm -rf ${CURDIR}/micro1-grpc/src/*_pb2*
	cp -a ${BUILD_DIR}/proto_grpc/* ${CURDIR}/gateway/src/
	cp -a ${BUILD_DIR}/proto_grpc/* ${CURDIR}/micro1-grpc/src/

.PHONY: clean
clean:
	rm -rf ${VENV_DIR}
	rm -rf ${BUILD_DIR}
	rm -rf ${CURDIR}/gateway/src/__pycache__
	rm -rf ${CURDIR}/micro1-grpc/src/__pycache__
	rm -rf ${CURDIR}/micro1-mom/src/__pycache__
	rm -rf ${CURDIR}/mom-setup/__pycache__
	rm -rf ${CURDIR}/gateway/src/*_pb2*
	rm -rf ${CURDIR}/micro1-grpc/src/*_pb2*
	rm -rf ${CURDIR}/micro2-mom/src/*_pb2*
