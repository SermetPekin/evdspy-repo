
from .load_commands_cmds_to_load import get_df_datagroup
from evdspy import *
df_exchange_rate = get_df_datagroup(
    datagroup="bie_dkdovytl",
    start_date='01-01-2010',
    end_date='01-01-2030',
)