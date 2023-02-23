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
	mkdir -p ${BUILD_DIR}/proto_grpc
	${PYBIN} -m grpc_tools.protoc -Iprotos --python_out=${BUILD_DIR}/proto_grpc --pyi_out=${BUILD_DIR}/proto_grpc --grpc_python_out=${BUILD_DIR}/proto_grpc protos/message.proto
	rm -rf ${CURDIR}/gateway/src/proto_grpc
	rm -rf ${CURDIR}/micro1-grpc/src/proto_grpc
	cp -r ${BUILD_DIR}/proto_grpc ${CURDIR}/gateway/src/
	cp -r ${BUILD_DIR}/proto_grpc ${CURDIR}/micro1-grpc/src/

.PHONY: clean
clean:
	rm -rf ${VENV_DIR}
	rm -rf ${BUILD_DIR}
	rm -rf ${CURDIR}/gateway/src/__pycache__
	rm -rf ${CURDIR}/micro1-grpc/src/__pycache__
	rm -rf ${CURDIR}/gateway/src/proto_grpc
	rm -rf ${CURDIR}/micro1-grpc/src/proto_grpc
