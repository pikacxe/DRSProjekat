# Taskovi za DRS projekat



 - [ ] api/admin/register
 - [ ] api/admin/transactions
 - [ ] api/admin/verify
 - [ ] api/login
 - [ ] api/profile
 - [ ] api/profile/update
 - [ ] api/card/add
 - [ ] api/card/
 - [ ] api/card/:id
 - [ ] api/card/:id/deposit
 - [ ] api/transaction/add


## Entiteti

 - Admin
   - FirstName      :str
   - LastName       :str
   - Address        :str
   - City           :str
   - Country        :str
   - PhoneNumber    :str
   - Email          :str
   - Password       :str

 - User
   - UID            :int
   - FirstName      :str
   - LastName       :str
   - Address        :str
   - City           :str
   - Country        :str
   - PhoneNumber    :str
   - Email          :str
   - Password       :str
   - Cards []       :Array
   - _verified      :bool
   - _creationDate  :Date

 - Card
   - CardNumber     :str
   - UserID         :int
   - Currency       :str
   - Amount         :double
   - Currencies     :Array (0x00000000000000000000000010000001?)


 - Transaction
   - UID                    :str
   - SenderID               :int
   - SenderCardNumber       :str
   - Currency               :str (int? api number)
   - Amount                 :double
   - RecipientCardnumber    :str
   - RecipientEmail         :string
   - RecipientFName         :string
   - RecipientLName         :string
   - State                  :bool
