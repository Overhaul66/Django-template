import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import CustomUser, Customer, SalonManager, SalonEmployee
from apps.salons.models import Salon, SalonService
from apps.users.services import register_user
from apps.salons.services import create_salon, create_salon_service
from apps.appointments.services import create_appointment

class Command(BaseCommand):
    help = 'Seeds the database with sample managers, salons, services, employees and customers.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Clearing existing data...")
        CustomUser.objects.all().delete()
        Salon.objects.all().delete()
        
        self.stdout.write("Creating users...")
        
        # 1. Create Managers
        manager_user = register_user(
            email="manager@salon.com",
            password="password123",
            role="SALON_MANAGER",
            first_name="Alice",
            last_name="Smith",
            phone="1234567890"
        )
        manager = manager_user.manager_profile
        
        # 2. Create Salons
        self.stdout.write("Creating salons...")
        salon1 = create_salon(
            manager=manager,
            name="Glow & Co",
            phone="555-1111",
            email="glow@salon.com",
            address="123 Beauty Lane",
            city="Seattle",
            country="USA",
            opening_time=datetime.time(9, 0),
            closing_time=datetime.time(18, 0),
            gender_type="UNISEX"
        )
        
        salon2 = create_salon(
            manager=manager,
            name="Gentlemen's Cut",
            phone="555-2222",
            email="gents@salon.com",
            address="456 Grooming Blvd",
            city="Seattle",
            country="USA",
            opening_time=datetime.time(10, 0),
            closing_time=datetime.time(20, 0),
            gender_type="MEN_ONLY"
        )
        
        # 3. Create Services
        self.stdout.write("Creating salon services...")
        cut1 = create_salon_service(salon1, "Hair Cut", 30, 25.00)
        color1 = create_salon_service(salon1, "Hair Coloring", 90, 80.00)
        massage1 = create_salon_service(salon1, "Massage", 60, 60.00)
        
        cut2 = create_salon_service(salon2, "Shaving & Cut", 45, 35.00)
        beard2 = create_salon_service(salon2, "Beard Trim", 20, 15.00)
        
        # 4. Create Employees
        self.stdout.write("Creating employees...")
        emp_user1 = register_user(
            email="john.stylist@salon.com",
            password="password123",
            role="SALON_EMPLOYEE",
            first_name="John",
            last_name="Stylist",
            phone="555-0001",
            salon=salon1,
            position="Senior Stylist",
            bio="Haircut specialist with 10 years experience."
        )
        
        emp_user2 = register_user(
            email="mary.colorist@salon.com",
            password="password123",
            role="SALON_EMPLOYEE",
            first_name="Mary",
            last_name="Colorist",
            phone="555-0002",
            salon=salon1,
            position="Color Expert",
            bio="Master colorist trained in Paris."
        )

        emp_user3 = register_user(
            email="bob.barber@salon.com",
            password="password123",
            role="SALON_EMPLOYEE",
            first_name="Bob",
            last_name="Barber",
            phone="555-0003",
            salon=salon2,
            position="Barber",
            bio="Classic cuts and straight razor shave master."
        )
        
        # 5. Create Customers
        self.stdout.write("Creating customers...")
        cust_user1 = register_user(
            email="customer1@gmail.com",
            password="password123",
            role="CUSTOMER",
            first_name="Charles",
            last_name="Brown",
            phone="9876543210",
            gender="MALE",
            preferred_notification="EMAIL"
        )
        c1 = cust_user1.customer_profile
        
        cust_user2 = register_user(
            email="customer2@gmail.com",
            password="password123",
            role="CUSTOMER",
            first_name="Dana",
            last_name="Scully",
            phone="9876543211",
            gender="FEMALE",
            preferred_notification="BOTH"
        )
        c2 = cust_user2.customer_profile
        
        # 6. Book sample appointments
        self.stdout.write("Booking sample appointments...")
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        
        create_appointment(
            customer=c1,
            salon=salon1,
            service=cut1,
            date=tomorrow,
            start_time=datetime.time(10, 0),
            booking_notes="Looking forward to it!"
        )
        
        create_appointment(
            customer=c2,
            salon=salon1,
            service=cut1,
            date=tomorrow,
            start_time=datetime.time(10, 0),
            booking_notes="Need a quick trim."
        )
        
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write(f"Manager Account: manager@salon.com / password123")
        self.stdout.write(f"Employee (Glow & Co): john.stylist@salon.com / password123")
        self.stdout.write(f"Employee (Gents Cut): bob.barber@salon.com / password123")
        self.stdout.write(f"Customer 1 Account: customer1@gmail.com / password123")
