import string
import secrets
from datetime import datetime
from getpass import getpass


COMMON_PASSWORDS = {
    "password",
    "password123",
    "12345678",
    "123456789",
    "qwerty123",
    "admin123",
    "iloveyou",
    "welcome123",
    "abc123",
    "letmein"
}


def check_password(password):
    score = 0
    suggestions = []

    # 1. Password length
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append(
            "Use at least 12 characters."
        )

    # 2. Uppercase letters
    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append(
            "Add uppercase letters (A-Z)."
        )

    # 3. Lowercase letters
    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append(
            "Add lowercase letters (a-z)."
        )

    # 4. Numbers
    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append(
            "Add numbers (0-9)."
        )

    # 5. Special characters
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        suggestions.append(
            "Add special characters (!, @, #, etc.)."
        )

    # 6. Common password detection
    if password.lower() in COMMON_PASSWORDS:
        return "Weak", [
            "This is a commonly used password.",
            "Choose a unique password."
        ]

    # 7. Repeated character detection
    if len(password) >= 4 and len(set(password)) <= 2:
        return "Weak", [
            "Avoid passwords with repeated characters."
        ]

    # 8. Sequential pattern detection
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop"
    ]

    lower_password = password.lower()

    for sequence in sequences:
        for i in range(len(sequence) - 3):
            pattern = sequence[i:i + 4]

            if pattern in lower_password:
                suggestions.append(
                    "Avoid predictable sequential patterns."
                )
                score -= 1
                break

    # 9. Determine password strength
    if len(password) < 8 or score <= 2:
        strength = "Weak"

    elif len(password) >= 12 and score >= 6:
        strength = "Strong"

    else:
        strength = "Medium"

    return strength, suggestions


def generate_password(length=16):
    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    while True:
        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if (
            any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)
        ):
            return password


def save_report(strength, suggestions):
    filename = (
        "wifi_security_report_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".txt"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write("=" * 40 + "\n")
        file.write("WI-FI PASSWORD SECURITY AUDIT REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write(
            "Audit Date: "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "\n"
        )

        file.write(
            "Password Strength: "
            + strength
            + "\n\n"
        )

        file.write("Security Recommendations:\n")

        if suggestions:
            for suggestion in suggestions:
                file.write("- " + suggestion + "\n")
        else:
            file.write(
                "All basic checks passed.\n"
            )

        file.write(
            "\nNote: Password was not stored in this report.\n"
        )

        file.write(
            "This is an educational security auditing tool.\n"
        )

    print("\nReport saved successfully:", filename)


def audit_password():
    print("\n--- Wi-Fi Password Security Audit ---")

    password = getpass(
        "Enter a sample Wi-Fi password: "
    )

    if not password:
        print("Password cannot be empty.")
        return

    strength, suggestions = check_password(password)

    print("\nPassword Strength:", strength)

    if suggestions:
        print("\nSecurity Recommendations:")

        for suggestion in suggestions:
            print("-", suggestion)

    else:
        print(
            "\nGood! All basic checks passed."
        )

    save_report(strength, suggestions)


def password_generator():
    print("\n--- Secure Password Generator ---")

    try:
        length = int(
            input("Enter password length (12-64): ")
        )

        if length < 12 or length > 64:
            print(
                "Password length must be between 12 and 64."
            )
            return

        password = generate_password(length)

        print("\nGenerated Password:")
        print(password)

        print(
            "\nKeep this password private."
        )

    except ValueError:
        print("Please enter a valid number.")


def main():
    while True:
        print("\n")
        print("=" * 45)
        print(" WI-FI PASSWORD SECURITY AUDITOR")
        print("=" * 45)

        print("1. Audit Wi-Fi Password")
        print("2. Generate Secure Password")
        print("3. Exit")

        choice = input(
            "\nEnter your choice (1-3): "
        )

        if choice == "1":
            audit_password()

        elif choice == "2":
            password_generator()

        elif choice == "3":
            print(
                "\nThank you for using Wi-Fi Password Security Auditor."
            )
            break

        else:
            print(
                "\nInvalid choice. Please select 1, 2, or 3."
            )


if __name__ == "__main__":
    main()
