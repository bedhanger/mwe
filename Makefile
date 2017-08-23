all: deploy

deploy: whereto = $${HOME:-/tmp}
deploy: me      = mwe
deploy: what    = HEAD

deploy:
	@echo "Deploying ${what} into ${whereto}/${me}..."
	@git archive \
         --verbose \
         --format=tar \
         --prefix=${me}/ ${what} | ( cd ${whereto} && tar xf - )
