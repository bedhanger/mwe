all:
	${MAKE} deploy

deploy: whereto = $${HOME:-/tmp}
deploy: me      = mwe
deploy: what    = HEAD

deploy:
	@echo "Deploying ${what} into $(shell realpath ${whereto})/${me}..."
	@git archive \
         --verbose \
         --format=tar \
         --prefix=${me}/ ${what} | ( cd $(shell realpath ${whereto}) && tar xf - )
