class employee:
    def __init__(self,name,id):
        self.name = name
        self.id = id

    def print_info(self):
        print(f"name: {self.name} id: {self.id}")
        

class fulltime_employee(employee):
    def __init__(self,name,id,monthly_salary):
        super().__init__(name,id)
        self.monthly_salary = monthly_salary
        
    def calculate_salary(self):
        return self.monthly_salary

class parttime_employee(employee):
    def __init__(self,name,id,hourly_salary,work_days):
        super().__init__(name,id)
        self.hourly_salary = hourly_salary
        self.work_days = work_days
        
    def calculate_salary(self):
        return self.hourly_salary * self.work_days
    
emp1 = fulltime_employee("meow","87",10000)
emp2 = parttime_employee("haha","88",100,20)
emp1.print_info()
emp2.print_info()

print(emp1.calculate_salary())
print(emp2.calculate_salary())