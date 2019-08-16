# Build a simple md-based raid array.  Simple means we don't check for namespace
# collisions with regard to resources: dev id for the array, loop devices, container
# names...  Error handling is rather crude.

# md admin data
md_id		= 42
array		= /dev/md${md_id}

# Array specifics
raid_level	= 5
raid_devs	= 3
spare_devs	= 0

# Backing containers
containers	= {0..2}
container_size	= 100M

all : create detail show

create : clean
	@# Create containers
	@truncate --size=${container_size} ${containers}
	@# Turn containers into block devices
	@for f in ${containers}; do \
		losetup --find $${f}; \
	done
	@# Create the array (and start it rw)
	@mdadm  --create ${array} \
		--level=${raid_level} \
		--raid-devices=${raid_devs} \
		--spare-devices=${spare_devs} \
		--bitmap=internal \
		--consistency-policy=bitmap \
		/dev/loop[${containers}]

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
