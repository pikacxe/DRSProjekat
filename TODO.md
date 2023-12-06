# Taskovi za DRS projekat



 - [X] api/admin/register
 - [ ] api/admin/transactions
 - [X] api/admin/verify
 - [X] api/login
 - [X] api/profile
 - [ ] api/profile/update
 - [ ] api/card/add
 - [ ] api/card/
 - [ ] api/card/:id
 - [ ] api/card/:id/deposit
 - [ ] api/transaction/add


## Entiteti

 - User
   - ID             :str PK
   - FirstName      :str
   - LastName       :str
   - Address        :str
   - City           :str
   - Country        :str
   - PhoneNumber    :str
   - Email          :str
   - Password       :str
   - isVerified     :bool
   - isAdmin        :bool


 - Card
   - CardNumber     :str PK
   - UserID         :str FK


 - AccountBalance
   - CardNumber     :str PK (CardNumber, Currrency)
   - Currency       :str 
   - Balance        :double

 - Transaction
   - ID                     :str PK
   - SenderID               :int 
   - SenderCardNumber       :str 
   - Currency               :str
   - Amount                 :double
   - RecipientCardNumber    :str
   - RecipientEmail         :string
   - RecipientFName         :string
   - RecipientLName         :string
   - State                  :string
   - Created                :dateTime
   - Completed              :dateTime
   - isCompleted            :boolean
