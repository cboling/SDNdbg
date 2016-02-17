#!/bin/bash
#
# Script to assist in installing SDNdbg on a system
#
##################################################
# Create postgresql database
#
create_database()
{
    # TODO support parameters? (may want to create test database)
    # TODO support parameters? (may want to create test database)

    database=sdndbg_db
    username=sdn
    password=debugger

    sudo -u postgres createuser -w -SDR ${username}
    sudo -u postgres psql -U ${username} -d postgres -c "alter user postgres with password '${password}';"
    sudo -u postgres createdb -O ${username} ${database};
}

##################################################
# Activate the models for our apps
#
activate_models()
{
    # TODO Add all models here
    models=collector

    # Test run before executing

    python manage.py check || (echo "Issues found, models will not be activated" >&2 ; exit -1)

    # Activate

    python manage.py makemigrations # ${models}
    python manage.py migrate
}

##################################################
# Seed superuser name in djano database
#
seed_superuser()
{
    username=admin
    email=admin@example.com
    pwd=password

    echo "from django.contrib.auth.models import User; User.objects.create_superuser('${username}', '${email}', '${pwd}')" | python manage.py shell
}

##################################################
# Seed the database (or config)
#
seed_configuration()
{
    echo TODO Figure out what is best here
}


##################################################
# Run unit tests
#
run_unit_tests()
{
    echo TODO Implement test and coverage reports
}

# TODO Complete this
# TODO Add unit test support as part of 'setup'
# TODO Support multiple Linux distro's, not just on Ubuntu. Perhaps centos 7 next
# TODO Add function to pull in any dependencies
# TODO Support mariadb and mongodb
# TODO Add backup/restore capability
# TODO Add cleanup capability - Leaves packages in place but scrubs DB
# TODO Put into docker containers as an option
# TODO For OpenStack, investigate Horizon integration and tie-ins with Ceilometer/Telemetry, tacker, and others
# TODO Look at OPNFV projects for gaps we could fill (or make use of) such as copper, rs, doctor, promise, ...
