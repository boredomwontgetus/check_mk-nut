from .agent_based_api.v1 import *

battery_charge_ok = 98;
battery_charge_crit = 70;

wantedEntries = {'battery.charge': 'check_battery_charge',
                'battery.runtime': '',
                'ups.status': 'check_ups_status',
                'output.voltage':''
                }

def discover_nut_ups(section):
    for e in section:
      e[1] = e[1].replace(':', '')  
      if not e[1] in wantedEntries: continue
      yield Service(item=e[0]+' '+e[1])

def check_nut_ups(item, section):
    for e in section:
      e[1] = e[1].replace(':', '')  
      name = e[0]+' '+e[1]
      if not e[1] in wantedEntries:
        continue
      else:
        if name == item:
          if wantedEntries[e[1]]:
            s, value = eval(wantedEntries[e[1]] + "(e[2])")
          else:  
            s = State.OK
            value = ' '.join(e[2:])

          yield Result(state = s, summary = f"{value}")

def check_ups_status(value):
  if value == 'OL':
    s = State.OK
    val = 'ONLINE - Power connected'
  else:
    s = State.CRIT
    val = 'OFFLINE - Power disconnected'
  return(s, val)

def check_battery_charge(value):
  value = int(value)
  if value >= battery_charge_ok :
    s = State.OK
  elif value < battery_charge_ok:
    s = State.WARN
  elif value <= battery_charge_crit:
    s = State.CRIT
  val = f"Charge: {value}%"
  return(s, val)


#    for line in section:
#      line[1] = line[1].replace(':', '')  
#      active_item = ' '.join([line[i] for i in [0, 1]])
#      if line[0] + ' battery.charge' == item:
#        summary = line[2]
#        yield Result(state=State.OK, summary=f"{summary}")
#
#      if line[0] + ' battery.runtime' == item:
#        summary = line[2]
#        yield Result(state=State.OK, summary=f"{summary}")
#      return


register.check_plugin(
    name="nut",
    service_name="NUT UPS %s",
    discovery_function=discover_nut_ups,
    check_function=check_nut_ups,
)
