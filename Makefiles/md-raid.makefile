# Build a simple md-based raid array.  Simple means we don't check for namespace
# collisions with regard to resources: dev id for the array, loop devices, container
# names...  Error handling is rather crude.

# md admin data
md_id		= 42
array		= /dev/md${md_id}

# Array specifics
raid_level	= 5
raid_devs	= 3
spare_devs	= 1
total_devs	= $(shell expr ${raid_devs} + ${spare_devs})

# Backing containers
containers	= {1..${total_devs}}
container_size	= 1000M

# Options for building the array
create_opts += --level=${raid_level}
create_opts += --raid-devices=${raid_devs}
create_opts += --spare-devices=${spare_devs}
create_opts += --bitmap=internal
create_opts += --consistency-policy=bitmap

all : create detail show

create : clean containers loopdevs array

containers : df
	@# Create containers
	@truncate --size=${container_size} ${containers}

df :
	@# Check for enough free disk space
	@true # WIP, obviously...

loopdevs :
	@# Turn containers into block devices
	@for f in ${containers}; do \
		losetup /dev/loop$${f} $${f}; \
	done

array :
	@# Create the array (and start it rw)
	@mdadm --create ${array} ${create_opts} /dev/loop[${containers}]

show :
	-@cat /proc/mdstat

detail :
	-@mdadm --${@} ${array}

details : detail

readonly readwrite :
	-@mdadm --${@} ${array}

ro : readonly
rw : readwrite

# Undo create, in reverse order
clean : readonly
	-@mdadm --stop ${array}
	-@losetup --detach /dev/loop[${containers}]
	@rm --force ${containers}
