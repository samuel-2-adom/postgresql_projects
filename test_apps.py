import io
import uuid
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch

from contact_book.util import ContactBook
from contact_book.util import database as contact_database
from expense_tracker.util import ExpenseTracker
from expense_tracker.util import database as expense_database


class ContactBookIntegrationTests(TestCase):
    def setUp(self):
        suffix = uuid.uuid4().hex[:10]
        self.phone = str(uuid.uuid4().int % 10**12)
        self.first_name = f"Test{suffix}"
        self.last_name = "Contact"

    def tearDown(self):
        with contact_database.connect() as cursor:
            cursor.execute(
                "DELETE FROM contacts WHERE phone_number = %s",
                (self.phone,),
            )

    def test_add_and_display_contact_in_postgresql(self):
        contact_book = ContactBook(db=None)

        with redirect_stdout(io.StringIO()):
            contact_book.add_cont(
                self.first_name,
                self.last_name,
                self.phone,
                f"{self.first_name.lower()}@example.com",
            )

        with contact_database.connect() as cursor:
            cursor.execute(
                """SELECT first_name, last_name, phone_number
                FROM contacts WHERE phone_number = %s""",
                (self.phone,),
            )
            contact = cursor.fetchone()

        self.assertIsNotNone(contact, "Contact was not saved to PostgreSQL")
        self.assertEqual(contact["first_name"], self.first_name)
        self.assertEqual(contact["last_name"], self.last_name)

        output = io.StringIO()
        with redirect_stdout(output):
            has_contacts = contact_book.displ()

        self.assertTrue(has_contacts)
        self.assertIn(self.phone, output.getvalue())


class ExpenseTrackerIntegrationTests(TestCase):
    def setUp(self):
        self.description = f"electricity unittest {uuid.uuid4().hex}"
        self.amount = 37.25

    def tearDown(self):
        with expense_database.connect() as cursor:
            cursor.execute(
                "DELETE FROM expenses WHERE description = %s",
                (self.description,),
            )

    def test_add_and_load_expense_in_postgresql(self):
        expense_tracker = ExpenseTracker(db=None)

        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            expense_tracker.add_exp(self.amount, self.description)

        with expense_database.connect() as cursor:
            cursor.execute(
                """SELECT expenses.id, expenses.amount, categories.category
                FROM expenses
                JOIN categories ON categories.id = expenses.category_id
                WHERE expenses.description = %s""",
                (self.description,),
            )
            expense = cursor.fetchone()

        self.assertIsNotNone(expense, "Expense was not saved to PostgreSQL")
        self.assertEqual(float(expense["amount"]), self.amount)
        self.assertEqual(expense["category"], "Utilities")

        output = io.StringIO()
        with redirect_stdout(output):
            expense_tracker.load_exp(expense["id"])

        self.assertIn(self.description, output.getvalue())


if __name__ == "__main__":
    import unittest

    unittest.main()
