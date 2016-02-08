#!/bin/bash
#
# Script to assist in installing SDNdbg on a system
#
##################################################
# Create postgresql database
#
create_database()
{
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
    models=collector

    # Test run before executing

    python manage.py check || (echo "Issues found, models will not be activated" >&2 ; exit -1)

    # Activate

    python manage.py makemigrations ${models}
}


##################################################
# Seed the database (or config)
#
seed_configuration()
{
    echo TODO Figure out what is best here
}


# TODO Complete this and test it
