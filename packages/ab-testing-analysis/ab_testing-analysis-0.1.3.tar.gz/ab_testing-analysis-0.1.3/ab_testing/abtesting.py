# Import the required lib
import pandas 
import numpy as np


class ABTest:

    def __init__(self,df_A:pandas.DataFrame,response_column:str, df_B:pandas.DataFrame=None,
                            group_column:str=None,labels = ['A','B']) -> None:
        """
        The function takes in either one DataFrame or two dataframes, and a column name for the response
        variable. It then creates a new object with attributes for the two dataframes, the response
        variable, and the group labels
        
        :param df_A: The first dataframe
        :type df_A: pandas.DataFrame

        :param response_column: The column name of the response variable.
                                Value in the response column should be 0&1 to indicating the unsucessful and successful.
        :type response_column: str

        :param df_B: The second dataframe
        :type df_B: pandas.DataFrame

        :param group_column: The column name that indicates the group
        :type group_column: str

        :param labels: The labels for the two groups Optional
        """

        # Check the unique values in response column and raise error if not binary
        if df_A[response_column].nunique() !=2:
                ValueError('Response column should contain binary values')
        # Set the response column name 
        self.response_column = response_column

        # Check the group column is none or not it not means Single DF contain both A & B set
        if group_column !=None:
            # Set the group column
            self.group_column = group_column

            # Check the unique values in group_column and raise error if not binary
            if df_A[self.group_column].nunique() !=2:
                ValueError('Group column should contain two distinct values indicating A&B set')

            # Take group element values & Create two DF by slicing the Master DF
            self.groups_ele = list(df_A[self.group_column].unique())
            self.a_sample = df_A[df_A[self.group_column]==self.groups_ele[0]]
            self.b_sample  = df_A[df_A[self.group_column]==self.groups_ele[1]] 

            # Assgine the group element as Labels
            self.a_label = self.groups_ele[0]
            self.b_label = self.groups_ele[1]

        # Check if DF B is give or not
        elif df_B !=None:

            # Assigne the DF to right varibles
            self.b_sample = df_B
            self.a_sample = df_A
            
            # Assgine the labels either defaul or given by the user.
            self.a_label = labels[0]
            self.b_label = labels[1]

        # Check either DF B is given or group_column else raise the error.
        elif df_B ==None and group_column==None:
            ValueError('Either provide the second dataframe(df_B) or give column name for group indication of A&B') 

    def conversion_rate(self) -> pandas.DataFrame:
        """
        The function calculate theconversion rate, standard deviation,
        and standard error for each group and return DataFrame.

        :return: A dataframe with the conversion rate, standard deviation and standard error for each
        group.

        """

        # Calculate the Converation Rate of Sample and return in percentage for both A & B set
        conv_rt_a = f"{np.mean(self.a_sample[self.response_column]):.2%}"
        conv_rt_b = f"{np.mean(self.b_sample[self.response_column]):.2%}"  

        # Calculate the Standard Deviation and return in percentage for both A & B set
        std_a = f"{np.std(self.a_sample[self.response_column], ddof=0):.3}" 
        std_b = f"{np.std(self.b_sample[self.response_column], ddof=0):.3}"

        # Calculate the Standard Error and return in percentage for both A & B set
        std_err_a = f"{np.std(self.a_sample[self.response_column], ddof=1)/ np.sqrt(np.size(self.a_sample[self.response_column])):.3}"
        std_err_b = f"{np.std(self.b_sample[self.response_column], ddof=1)/ np.sqrt(np.size(self.b_sample[self.response_column])):.3}"
        
        # Create the final report on performace of the set
        conv_rt_report = pandas.DataFrame(data={"Conversion Rate":[conv_rt_a,conv_rt_b],
                                "Standard Deviation":[std_a,std_b],
                                "Standar Error":[std_err_a,std_err_b]},
                                index=[self.a_label,self.b_label]
        )
        
        return conv_rt_report