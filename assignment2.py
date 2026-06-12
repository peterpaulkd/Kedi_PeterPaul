#simple store for infomation
users = {
    "Kedi": ("admin123", "Admin"),
    "Peter": ("cust123", "Customer"),
    "Paul": ("cashier123", "Cashier"),
}

#valid coupon and discount percentages
valid_coupons = {
    "SAVE10": 10,
    "SAVE20": 20,
    "WELCOME5": 5,
}

#tax rates based on location
tax_rates = {
    "kampala": 13,
    "nairobi": 16,
    "other": 10,
}


#3 attempts max for login
user_role = None
attempts = 0

while user_role is None and attempts < 3:
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users: 
        correct_password, role = users[username]
        #password check
        if password == correct_password:
            print(f"Login successful, {username} ({role}).")
            user_role = role
        else:
            print("Invalid password.")
    else:
        print("Username not found.")
    attempts += 1
        
#stop if the user fails 3 times
if user_role is None:
    print("\n Access denied. Too many failed attempts.")

else:
    print(f"\n Welcome, {username} Logged in as {user_role}.")

    if user_role == "Admin":
        print("You have full access.")
        print("Manage products, view sales")
    
    elif user_role == "Cashier":
        print("You have Cashier access.")
        print("View all sales reports")

    elif user_role == "Customer":
        print("You have Customer access.")
        print("Browse products, apply coupons")

    
    #calculator allowed to everyone
    run_calc = input("\nWould you like to use the price calculator? (yes/no):").lower()

    if run_calc == "yes":
        print("\nPrice Calculator")

        #getting subtotal
        subtotal = float(input("Enter the subtotal: "))

        #cooupon code check
        coupon_code = input("Enter coupon code (or press Enter to skip): ").strip().upper()
        coupon_discount = 0

        if coupon_code == "":
            print("No coupon entered.")
        else:
            if coupon_code in valid_campus:
                coupon_discount = valid_coupons[coupon_code]
                print(f"Coupon valid! {coupon_discount}% off.")
            else:
                print("Invalid coupon code. No coupon discount")

        #volume based discount
        volume_discount = 0
        if subtotal >= 1000:
            volume_discount = 5
        elif subtotal >= 5000:
            volume_discount = 10
        elif subtotal >= 10000:
            volume_discount = 15

        if volume_discount > 0:
            print(f"Volume discount applied: {volume_discount}% off.")
        else:
            print("No volume discount applied.")

        #location based tax
        location = input("Enter your location (Kampala/Nairobi/Other): ").strip().lower()

        if location in tax_rates:
            tax_rate = tax_rates[location]
        else:
            tax_rate = tax_rates["other"]

        print(f"Tax rate for location is {tax_rate}%.")


        #calculations
        total_discount_percent = coupon_discount + volume_discount

        #business logic 
        if total_discount_percent > 50:
            total_discount_percent = 50
            print("Total discount capped at 50%.")

        discount_amount = subtotal * (total_discount_percent / 100)
        discounted_price = subtotal - discount_amount

        tax_amount = discounted_price * (tax_rate / 100)
        final_price = discounted_price + tax_amount

        #display for the final price breakdown
        print("\nPrice Breakdown:")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: ${discount_amount:.2f}")
        print(f"Discounted Price: ${discounted_price:.2f}")
        print(f"Tax ({tax_rate}%): ${tax_amount:.2f}")
        print(f"Final Price: ${final_price:.2f}")

    else:
        print("\nSystem existing.")