import messagebird

ACCESS_KEY = "TAu4RUJ4kp4CGgDxmoDiiFPdM"

client = messagebird.Client(ACCESS_KEY)
message = client.message_create(
          'GHS-HOLDING',
          '22548566846',
          'Salut, Bienvenus sur GHS',
          # { 'reference' : 'Foobar' }
      )