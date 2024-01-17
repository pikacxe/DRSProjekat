# Taskovi za DRS projekat



 - [X] api/admin/register
 - [X] api/admin/transactions
    - [X] implement flask-socketio for real-time transaction view
 - [X] complete pending transactions with process
    - [X] send mail on transaction complete
 - [X] api/admin/users
 - [X] api/admin/verify
    - [X] send mail on user verify
 - [X] api/login
 - [X] api/change-password
 - [X] api/profile
 - [X] api/profile/update
 - [X] api/card/add
 - [X] api/card/
 - [X] api/card/:id
 - [X] api/card/:id/deposit
 - [X] api/transaction/add
 


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
   - CardNumber     :str PK
   - Currency       :str PK
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
