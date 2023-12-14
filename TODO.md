# Taskovi za DRS projekat



 - [X] api/admin/register
    - [ ] add password hashing
 - [ ] api/admin/transactions
    - [ ] send mail on transaction complete
    - [ ] implement flask-socketio for real-time transaction view
 - [X] api/admin/users
 - [X] api/admin/verify
    - [X] send mail on user verify
 - [X] api/login
 - [X] api/profile
 - [ ] api/profile/update
 - [X] api/card/add
 - [X] api/card/
 - [X] api/card/:id
 - [X] api/card/:id/deposit
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
