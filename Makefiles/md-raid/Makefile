# Build a simple md-based raid array.  Simple means we don't check for namespace
# collisions with regard to resources: dev id for the array, loop devices, container
# names...  Error handling is rather crude.

# md admin data
id		= 42
md_id		= md${id}
array		= /dev/${md_id}
config		= $(shell realpath ${md_id}.conf)

# Array specifics
raid_level	= 5
raid_devs	= 3
spare_devs	= 1
total_devs	= $(shell expr ${raid_devs} + ${spare_devs})

# Backing containers
containers	= {1..${total_devs}}
container_size	= 1000MiB

# Free disk space considerations, 5% margin on top...
nrm_cnt_size	= $(shell humanfriendly --parse-size=${container_size})
what_we_need	= $(shell bc --mathlib <<<"scale=0; (${total_devs} * ${nrm_cnt_size} * 105) / 100")
what_we_have	= $(shell df --block-size=1 --output=avail . | tail --lines=1)

# Options for building the array
create_opts += --level=${raid_level}
create_opts += --raid-devices=${raid_devs}
create_opts += --spare-devices=${spare_devs}
create_opts += --bitmap=internal
create_opts += --consistency-policy=bitmap

all : create detail show

create : clean containers loopdevs array ${config}

${config} :
	mdadm --detail --scan | rg ${array} | tee ${@}

containers : df
	@# Create containers
	truncate --size=${container_size} ${containers}

df :
	@# Check for enough free disk space
	@if [ ${what_we_need} -gt ${what_we_have} ]; then \
		echo "Need more free disk space in this folder: $(shell humanfriendly --binary \
			--format-size=${what_we_need}) \
(only have $(shell humanfriendly --binary --format-size=${what_we_have}))"; \
		false; \
	fi

loopdevs :
	@# Turn containers into block devices
	@for f in ${containers}; do \
		losetup --verbose /dev/loop$${f} $${f}; \
	done

array :
	@# Create the array (and start it rw)
	mdadm --create ${array} ${create_opts} /dev/loop[${containers}]

show :
	-cat /proc/mdstat

details : detail

readonly readwrite detail stop assemble :
	-mdadm --${@} --config=${config} ${array}

ro : readonly
rw : readwrite

synx : sync
sync :
	${@}
	${@}
	${@}

# Undo create, in reverse order
clean : synx readonly stop release remove

release :
	-losetup --verbose --detach /dev/loop[${containers}]

remove :
	rm --force --verbose ${containers} ${config}
