from django.db import models



class Transaction(models.Model):
    """
    Represents a single transaction into or out of a payment method and a brief
    description of the transaction.

    Attributes:
        date - The date the transaction was made.
        transaction_method - The transaction method which was used.
        retailer - The other party involved in the transaction.
        total - The total ammount of the transaction (including tax). Postive numbers
                indicate that the user is ganing money, negative numbers indicate that
                the user has spent money.
        tax - The ammount of the transaction that was tax.
        description - A breif desctiption of what the transaction was for.
        categories - The categories to which the transaction belongs.
    """
    date = models.DateField()
    transaction_method = models.ForeignKey('TransactionMethod', on_delete=models.PROTECT)
    retailer = models.ForeignKey('Retailer', on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=11, decimal_places=2)
    tax = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    categories = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return '{0} - {1}'.format(str(self.retailer), str(self.description))



class TransactionMethod(models.Model):
    """
    Represents a payment method.
    For example: Cash, TCF Checking Account, Parents.

    Attributes:
        name - The name of the transaction method (see above examples).
    """
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name



class Retailer(models.Model):
    """
    Represents a retailer who is either reciving or giving the transaction.

    Attributes:
        name - The name of the retailer.
    """
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name



class Category(models.Model):
    """
    Represents a category (or sub-category) of transactions. Related to transactions
    in a many-to-many relationship.

    Attributes:
        name - The name of the [sub]category. If null then the category is a top-most
               category (has no parents).
        parent - The parent category.
    """
    name = models.CharField(max_length=300)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name
