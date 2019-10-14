.PHONY: sources

SPEC_FILE=zrepl.spec

sources:
	spectool -g ${SPEC_FILE}

srpm:
	rpmbuild -bs ${SPEC_FILE} \
	    -D "_sourcedir ${PWD}" \
	    -D "_srcrpmdir ${PWD}"
