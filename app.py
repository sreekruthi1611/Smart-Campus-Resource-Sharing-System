import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os


st.set_page_config(
    page_title="Smart Campus Resource Sharing System",
    page_icon="🏫",
    layout="wide"
)


# ---------------- DATA ----------------

if "resources" not in st.session_state:

    st.session_state.resources = pd.DataFrame({

    "Item":[
    "Scientific Calculator",
    "Umbrella",
    "Laptop Charger",
    "Lab Coat",
    "Power Bank",
    "First Aid Kit",
    "Arduino Kit",
    "USB Drive"
    ],

    "Category":[
    "Academic Items",
    "Emergency Resources",
    "Electronics",
    "Lab Equipment",
    "Electronics",
    "Emergency Resources",
    "Lab Equipment",
    "Academic Items"
    ],

    "Available":[15,10,8,12,6,5,4,20]

    })



images={

"Scientific Calculator":"images/calculator.jpg",
"Umbrella":"images/umbrella.jpg",
"Laptop Charger":"images/charger.jpg",
"Lab Coat":"images/labcoat.jpg",
"Power Bank":"images/powerbank.jpg",
"First Aid Kit":"images/firstaid.jpg",
"Arduino Kit":"images/arduino.jpg",
"USB Drive":"images/usb.jpg"

}



penalties=pd.DataFrame({

"Roll Number":[
"22A91A0001",
"22A91A0002"
],

"Student":[
"Rithika",
"Rahul"
],

"Item":[
"Calculator",
"Umbrella"
],

"Days Late":[
2,
1
],

"Fine":[
40,
20
]

})



# ---------------- SESSION ----------------


if "role" not in st.session_state:
    st.session_state.role=None

if "student_login" not in st.session_state:
    st.session_state.student_login=False

if "admin_login" not in st.session_state:
    st.session_state.admin_login=False

if "borrowings" not in st.session_state:
    st.session_state.borrowings=pd.DataFrame(
        columns=["Item","Due Date","Status"]
    )

if "borrow_item" not in st.session_state:
    st.session_state.borrow_item=None




# ---------------- ROLE ----------------


if st.session_state.role is None:


    st.title(
        "🏫 Smart Campus Resource Sharing System"
    )


    a,b=st.columns(2)


    with a:

        if st.button(
            "👨‍🎓 Student",
            use_container_width=True
        ):

            st.session_state.role="student"
            st.rerun()


    with b:

        if st.button(
            "👨‍💼 Admin",
            use_container_width=True
        ):

            st.session_state.role="admin"
            st.rerun()





# =================================================
# STUDENT
# =================================================


elif st.session_state.role=="student":


    if not st.session_state.student_login:


        st.title(
            "👨‍🎓 Student Login"
        )


        option=st.radio(
            "Option",
            [
            "Sign In",
            "Sign Up"
            ]
        )


        if option=="Sign Up":

            st.text_input("Name")
            st.text_input("Email")
            st.text_input("Password",type="password")


            if st.button("Create Account"):

                st.success(
                    "Account created successfully"
                )


        else:


            email=st.text_input("Email")
            password=st.text_input(
                "Password",
                type="password"
            )


            if st.button("Sign In"):


                if email and password:

                    st.session_state.student_login=True
                    st.rerun()

                else:

                    st.warning(
                        "Enter details"
                    )



    else:


        page=st.sidebar.selectbox(
            "Menu",
            [
            "Dashboard",
            "Catalog",
            "My Borrowings",
            "Return Item",
            "Notifications"
            ]
        )



        if page=="Dashboard":


            st.title(
                "🏠 Student Dashboard"
            )


            search=st.text_input(
                "Search Resource"
            )


            category=st.selectbox(
                "Category",
                [
                "All",
                "Academic Items",
                "Lab Equipment",
                "Electronics",
                "Emergency Resources"
                ]
            )


            filtered=st.session_state.resources.copy()



            if search:


                result=filtered[
                    filtered.Item.str.contains(
                        search,
                        case=False
                    )
                ]


                if not result.empty:

                    filtered=result

                    st.info(
                        "Category updated automatically"
                    )


                else:

                    st.warning(
                        "No resource found"
                    )

                    filtered=filtered.iloc[0:0]



            elif category!="All":

                filtered=filtered[
                    filtered.Category==category
                ]



            if not filtered.empty:

                item=st.selectbox(
                    "Select Item",
                    filtered.Item
                )


                row=filtered[
                    filtered.Item==item
                ].iloc[0]


                st.write(
                    "Category:",
                    row.Category
                )

                st.write(
                    "Available:",
                    row.Available
                )



                if st.button("Borrow Now"):

                    st.session_state.borrow_item=item
        # -------- BORROW CONFIRMATION --------


        if st.session_state.borrow_item:


            st.divider()


            st.success(
                "Borrow Confirmation"
            )


            agree=st.checkbox(
                "I agree to return the item on time"
            )


            if st.button(
                "Confirm Borrow"
            ):


                if agree:


                    new=pd.DataFrame({

                    "Item":[
                    st.session_state.borrow_item
                    ],

                    "Due Date":[
                    str(date.today()+timedelta(days=3))
                    ],

                    "Status":[
                    "Active"
                    ]

                    })


                    st.session_state.borrowings=pd.concat(
                        [
                        st.session_state.borrowings,
                        new
                        ],
                        ignore_index=True
                    )


                    st.session_state.resources.loc[
                        st.session_state.resources.Item==
                        st.session_state.borrow_item,
                        "Available"
                    ]-=1



                    st.success(
                        "Borrowed Successfully"
                    )


                    st.session_state.borrow_item=None

                    st.rerun()


                else:

                    st.warning(
                        "Accept policy first"
                    )





        # ---------------- CATALOG ----------------


        elif page=="Catalog":


            st.title(
                "📚 Resource Catalog"
            )


            for _,row in st.session_state.resources.iterrows():


                st.subheader(
                    row.Item
                )


                st.write(
                    "Category:",
                    row.Category
                )


                st.write(
                    "Available:",
                    row.Available
                )


                if st.button(
                    f"Borrow {row.Item}"
                ):


                    st.session_state.borrow_item=row.Item

                    st.rerun()


                st.divider()





        # ---------------- BORROWINGS ----------------


        elif page=="My Borrowings":


            st.title(
                "📋 My Borrowings"
            )


            if st.session_state.borrowings.empty:


                st.info(
                    "No borrowed items"
                )


            else:


                st.dataframe(
                    st.session_state.borrowings,
                    use_container_width=True
                )






        # ---------------- RETURN ----------------


        elif page=="Return Item":


            st.title(
                "↩ Return Item"
            )



            if st.session_state.borrowings.empty:


                st.info(
                    "No items to return"
                )


            else:


                selected=st.selectbox(
                    "Select Item",
                    st.session_state.borrowings.Item
                )


                confirm=st.checkbox(
                    "Confirm Return"
                )


                if st.button(
                    "Complete Return"
                ):


                    if confirm:


                        st.session_state.borrowings=(
                            st.session_state.borrowings[
                            st.session_state.borrowings.Item!=selected
                            ]
                        )


                        st.session_state.resources.loc[
                            st.session_state.resources.Item==selected,
                            "Available"
                        ]+=1



                        st.success(
                            "Returned Successfully"
                        )


                        st.rerun()



                    else:

                        st.warning(
                            "Confirm return"
                        )





        # ---------------- NOTIFICATIONS ----------------


        elif page=="Notifications":


            st.title(
                "🔔 Notifications"
            )


            st.info(
                "No notifications"
            )
# =================================================
# ADMIN
# =================================================


elif st.session_state.role=="admin":


    if not st.session_state.admin_login:


        st.title(
            "👨‍💼 Admin Login"
        )


        username=st.text_input(
            "Username"
        )


        password=st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Login"
        ):


            # accepts any values

            st.session_state.admin_login=True
            st.rerun()



    else:


        page=st.sidebar.selectbox(
            "Admin Menu",
            [
            "Dashboard",
            "Inventory Management",
            "Penalty Management"
            ]
        )



        # -------- ADMIN DASHBOARD --------


        if page=="Dashboard":


            st.title(
                "👨‍💼 Admin Dashboard"
            )


            c1,c2,c3,c4=st.columns(4)


            c1.metric(
                "Total Items",
                len(st.session_state.resources)
            )


            c2.metric(
                "Borrowed",
                len(st.session_state.borrowings)
            )


            c3.metric(
                "Available",
                int(
                    st.session_state.resources.Available.sum()
                )
            )


            c4.metric(
                "Penalties",
                len(penalties)
            )





        # -------- INVENTORY --------


        elif page=="Inventory Management":


            st.title(
                "📦 Inventory Management"
            )


            st.subheader(
                "Current Inventory"
            )


            st.dataframe(
                st.session_state.resources,
                use_container_width=True
            )



            st.divider()



            st.subheader(
                "Add New Resource"
            )


            item=st.text_input(
                "Item Name"
            )


            category=st.selectbox(
                "Category",
                [
                "Academic Items",
                "Lab Equipment",
                "Electronics",
                "Emergency Resources"
                ]
            )


            quantity=st.number_input(
                "Quantity",
                min_value=1
            )



            if st.button(
                "➕ Add Item"
            ):


                if item:


                    new_item=pd.DataFrame({

                    "Item":[item],

                    "Category":[category],

                    "Available":[quantity]

                    })



                    st.session_state.resources=pd.concat(
                        [
                        st.session_state.resources,
                        new_item
                        ],
                        ignore_index=True
                    )



                    st.success(
                        "Item added successfully"
                    )


                    st.rerun()



                else:


                    st.warning(
                        "Enter item name"
                    )






        # -------- PENALTY --------


        elif page=="Penalty Management":


            st.title(
                "💰 Penalty Management"
            )


            st.dataframe(
                penalties,
                use_container_width=True
            )





# =================================================
# SIGN OUT
# =================================================


if st.session_state.role is not None:


    st.sidebar.divider()


    if st.sidebar.button(
        "🚪 Sign Out"
    ):


        st.session_state.role=None

        st.session_state.student_login=False

        st.session_state.admin_login=False

        st.session_state.borrow_item=None

        st.rerun()