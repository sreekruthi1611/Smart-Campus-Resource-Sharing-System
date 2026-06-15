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

resources = pd.DataFrame({

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


images = {

"Scientific Calculator":"images/calculator.jpg",
"Umbrella":"images/umbrella.jpg",
"Laptop Charger":"images/charger.jpg",
"Lab Coat":"images/labcoat.jpg",
"Power Bank":"images/powerbank.jpg",
"First Aid Kit":"images/firstaid.jpg",
"Arduino Kit":"images/arduino.jpg",
"USB Drive":"images/usb.jpg"

}


penalties = pd.DataFrame({

"Student":[
"Rithika",
"Rahul"
],

"Item":[
"Calculator",
"Umbrella"
],

"Days Late":[
2,1
],

"Fine":[
40,20
]

})


# ---------------- SESSION ----------------


if "role" not in st.session_state:
    st.session_state.role=None

if "student_login" not in st.session_state:
    st.session_state.student_login=False

if "admin_login" not in st.session_state:
    st.session_state.admin_login=False

if "borrow_popup" not in st.session_state:
    st.session_state.borrow_popup=False

if "my_borrowings" not in st.session_state:
    st.session_state.my_borrowings=pd.DataFrame(
        columns=["Item","Due Date","Status"]
    )



# ---------------- ROLE SELECT ----------------


if st.session_state.role is None:


    st.title(
        "🏫 Smart Campus Resource Sharing System"
    )


    st.subheader(
        "Select Your Role"
    )


    c1,c2=st.columns(2)


    with c1:

        if st.button(
            "👨‍🎓 Student",
            use_container_width=True
        ):

            st.session_state.role="student"
            st.rerun()



    with c2:

        if st.button(
            "👨‍💼 Admin",
            use_container_width=True
        ):

            st.session_state.role="admin"
            st.rerun()



# =====================================================
# STUDENT
# =====================================================


elif st.session_state.role=="student":


    if not st.session_state.student_login:


        st.title(
            "👨‍🎓 Student Account"
        )


        option=st.radio(
            "Choose",
            [
                "Sign In",
                "Sign Up"
            ]
        )



        if option=="Sign Up":


            name=st.text_input(
                "Name"
            )


            email=st.text_input(
                "Email"
            )


            password=st.text_input(
                "Password",
                type="password"
            )


            if st.button(
                "Create Account"
            ):


                if email and password:

                    st.success(
                        "Account created successfully. Sign In now."
                    )

                else:

                    st.warning(
                        "Fill details"
                    )



        else:


            email=st.text_input(
                "Email"
            )


            password=st.text_input(
                "Password",
                type="password"
            )


            if st.button(
                "Sign In"
            ):


                if email and password:


                    st.session_state.student_login=True

                    st.success(
                        "Login Successful"
                    )

                    st.rerun()


                else:

                    st.warning(
                        "Enter any values"
                    )



    else:



        page=st.sidebar.selectbox(
            "Menu",
            [
                "Dashboard",
                "Catalog",
                "Item Details",
                "My Borrowings",
                "Notifications",
                "Return Item"
            ]
        )



        # ---------------- DASHBOARD ----------------


        if page=="Dashboard":


            st.title(
                "🏠 Student Dashboard"
            )


            search=st.text_input(
                "🔍 Search Resource"
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


            filtered=resources.copy()



            if search:


                result=resources[
                    resources.Item.str.contains(
                        search,
                        case=False
                    )
                ]


                if not result.empty:


                    new_category=result.iloc[0].Category


                    st.info(
                        f"Category updated to {new_category}"
                    )


                    filtered=result


                else:


                    st.warning(
                        "No matching resource found"
                    )

                    filtered=resources.iloc[0:0]



            elif category!="All":


                filtered=filtered[
                    filtered.Category==category
                ]



            if not filtered.empty:


                selected=st.selectbox(
                    "Select Resource",
                    filtered.Item
                )


                item=filtered[
                    filtered.Item==selected
                ].iloc[0]


                a,b=st.columns(2)


                with a:

                    if os.path.exists(images[selected]):

                        st.image(
                            images[selected],
                            width=220
                        )


                with b:

                    st.subheader(selected)


                    st.write(
                        "Category:",
                        item.Category
                    )


                    st.write(
                        "Available:",
                        item.Available
                    )


                    st.write(
                        "Condition: Good"
                    )
                if st.button(
                    "🛒 Borrow Now"
                ):


                    st.session_state.borrow_popup=True

                    st.session_state.selected=selected



                if st.session_state.borrow_popup:


                    st.divider()


                    st.success(
                        "Borrow Confirmation"
                    )


                    st.write(
                        "Item:",
                        st.session_state.selected
                    )


                    st.write(
                        "Borrow Date:",
                        date.today()
                    )


                    st.write(
                        "Return Date:",
                        date.today()+timedelta(days=3)
                    )


                    agree=st.checkbox(
                        "I agree to return on time"
                    )


                    if st.button(
                        "Confirm Borrow"
                    ):


                        if agree:


                            new=pd.DataFrame({

                            "Item":[
                            st.session_state.selected
                            ],

                            "Due Date":[
                            str(date.today()+timedelta(days=3))
                            ],

                            "Status":[
                            "Active"
                            ]

                            })


                            st.session_state.my_borrowings=pd.concat(
                                [
                                st.session_state.my_borrowings,
                                new
                                ],
                                ignore_index=True
                            )


                            resources.loc[
                                resources.Item==st.session_state.selected,
                                "Available"
                            ]-=1


                            st.success(
                                "Borrowed Successfully"
                            )


                            st.session_state.borrow_popup=False

                            st.rerun()



                        else:

                            st.warning(
                                "Accept return policy"
                            )




        # ---------------- CATALOG ----------------


        elif page=="Catalog":


            st.title(
                "📚 Resource Catalog"
            )


            for _,r in resources.iterrows():


                st.subheader(
                    r.Item
                )


                if os.path.exists(images[r.Item]):

                    st.image(
                        images[r.Item],
                        width=150
                    )


                st.write(
                    "Category:",
                    r.Category
                )


                st.write(
                    "Available:",
                    r.Available
                )


                if st.button(
                    f"Borrow {r.Item}"
                ):


                    st.session_state.selected=r.Item

                    st.session_state.borrow_popup=True

                    st.rerun()


                st.divider()




        # ---------------- DETAILS ----------------


        elif page=="Item Details":


            st.title(
                "📦 Item Details"
            )


            item=st.selectbox(
                "Select Item",
                resources.Item
            )


            if os.path.exists(images[item]):

                st.image(
                    images[item],
                    width=250
                )


            row=resources[
                resources.Item==item
            ].iloc[0]


            st.write(
                "Category:",
                row.Category
            )


            st.write(
                "Availability:",
                row.Available
            )


            st.write(
                "Borrow Duration: 3 Days"
            )


            st.write(
                "Penalty: ₹20/day"
            )




        # ---------------- BORROWINGS ----------------


        elif page=="My Borrowings":


            st.title(
                "📋 My Borrowings"
            )


            if st.session_state.my_borrowings.empty:


                st.info(
                    "No borrowings yet"
                )


            else:


                st.dataframe(
                    st.session_state.my_borrowings,
                    use_container_width=True
                )





        # ---------------- NOTIFICATIONS ----------------


        elif page=="Notifications":


            st.title(
                "🔔 Notifications"
            )


            st.info(
                "No new notifications"
            )





        # ---------------- RETURN ----------------


        elif page=="Return Item":


            st.title(
                "↩ Return Item"
            )


            if st.session_state.my_borrowings.empty:


                st.info(
                    "No items to return"
                )


            else:


                st.dataframe(
                    st.session_state.my_borrowings,
                    use_container_width=True
                )



                selected_return=st.selectbox(
                    "Select Item To Return",
                    st.session_state.my_borrowings.Item
                )



                row=st.session_state.my_borrowings[
                    st.session_state.my_borrowings.Item==selected_return
                ].iloc[0]



                due=pd.to_datetime(
                    row["Due Date"]
                ).date()



                fine=0


                if date.today()>due:


                    late=(date.today()-due).days

                    fine=late*20


                    st.warning(
                        f"Late by {late} day(s)"
                    )


                    st.error(
                        f"Penalty ₹{fine}"
                    )


                    paid=st.checkbox(
                        "Pay Penalty"
                    )


                else:

                    paid=True



                confirm=st.checkbox(
                    "Confirm Return"
                )



                if st.button(
                    "Complete Return"
                ):


                    if confirm and paid:


                        st.session_state.my_borrowings = (
                            st.session_state.my_borrowings[
                            st.session_state.my_borrowings.Item
                            != selected_return
                            ]
                        )


                        resources.loc[
                            resources.Item==selected_return,
                            "Available"
                        ]+=1


                        st.success(
                            "Returned Successfully"
                        )


                        st.rerun()


                    else:


                        st.warning(
                            "Confirm return first"
                        )
# =====================================================
# ADMIN
# =====================================================


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


            # Accept any values

            st.session_state.admin_login=True

            st.rerun()



    else:



        page=st.sidebar.selectbox(
            "Admin Menu",
            [
            "Dashboard",
            "Inventory",
            "Penalty Management"
            ]
        )



        if page=="Dashboard":


            st.title(
                "👨‍💼 Admin Dashboard"
            )


            a,b,c,d=st.columns(4)


            a.metric(
                "Total Resources",
                len(resources)
            )


            b.metric(
                "Borrowed",
                len(st.session_state.my_borrowings)
            )


            c.metric(
                "Overdue",
                0
            )


            d.metric(
                "Available",
                int(resources.Available.sum())
            )




        elif page=="Inventory":


            st.title(
                "📦 Inventory Management"
            )


            st.dataframe(
                resources,
                use_container_width=True
            )


            new_item=st.text_input(
                "Add Item"
            )


            qty=st.number_input(
                "Quantity",
                min_value=1
            )


            if st.button(
                "Add Item"
            ):


                if new_item:


                    new_row=pd.DataFrame({

                    "Item":[new_item],

                    "Category":[
                    "Academic Items"
                    ],

                    "Available":[qty]

                    })


                    resources=pd.concat(
                        [
                        resources,
                        new_row
                        ],
                        ignore_index=True
                    )


                    st.success(
                        "Item Added"
                    )





        elif page=="Penalty Management":


            st.title(
                "💰 Penalty Management"
            )


            st.dataframe(
                penalties,
                use_container_width=True
            )





# ---------------- SIGN OUT ----------------


if st.session_state.role is not None:


    st.sidebar.divider()


    if st.sidebar.button(
        "🚪 Sign Out"
    ):


        st.session_state.role=None

        st.session_state.student_login=False

        st.session_state.admin_login=False

        st.session_state.borrow_popup=False


        st.rerun()