import dns.resolver

try:
    answers = dns.resolver.resolve(
        "_mongodb._tcp.cluster0.ziqqbvm.mongodb.net",
        "SRV"
    )

    for answer in answers:
        print(answer)

except Exception as e:
    print("DNS ERROR:", repr(e))