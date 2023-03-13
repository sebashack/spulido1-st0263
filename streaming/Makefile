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

.PHONY: build-proto
build-proto:
	rm -rf ${BUILD_DIR}/proto_grpc
	mkdir -p ${BUILD_DIR}/proto_grpc
	${PYBIN} -m grpc_tools.protoc -Iprotos --python_out=${BUILD_DIR}/proto_grpc --pyi_out=${BUILD_DIR}/proto_grpc --grpc_python_out=${BUILD_DIR}/proto_grpc protos/file_service.proto
	rm -rf ${CURDIR}/client/src/*_pb2*
	rm -rf ${CURDIR}/server/src/*_pb2*
	cp -a ${BUILD_DIR}/proto_grpc/* ${CURDIR}/client/src/
	cp -a ${BUILD_DIR}/proto_grpc/* ${CURDIR}/server/src/

.PHONY: clean
clean:
	rm -rf ${VENV_DIR}
	rm -rf ${BUILD_DIR}
	rm -rf ${CURDIR}/client/src/__pycache__
	rm -rf ${CURDIR}/client/src/*_pb2*
	rm -rf ${CURDIR}/server/src/__pycache__
	rm -rf ${CURDIR}/server/src/*_pb2*
