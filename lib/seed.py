#!/usr/bin/env python3

# Script goes here!


from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dev, Company, Freebie


if __name__ == '__main__':
    engine = create_engine('sqlite:///many_to_many.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Dev).delete()
    session.query(Company).delete()
    session.query(Freebie).delete()

    fake = Faker()


    devs = []

    for i in range(50):
        dev = Dev(name=fake.unique.name())

        session.add(dev)
        session.commit()
        devs.append(dev)

    companies = []
    
    for i in range(50):
        company = Company(
            name = fake.unique.name(),
            founding_year = random.randint(1900, fake.year())
            )
        session.add(company)
        session.commit()
        companies.append(company)
        
    freebies = []

    for company in companies:
        for i in random.randint(1,6):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()
            
            freebie = Freebie(
                
                item_name = fake.name(),
                value = fake.currency(),

                dev_id = dev.id,
                company_id = company.id
            )

            freebies.append(freebie)


    session.bulk_save_objects(freebies)
    session.commit()



    # session.bulk_save_objects(reviews)
    # session.commit()
    # session.close()