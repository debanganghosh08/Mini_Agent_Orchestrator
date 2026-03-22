import asyncio
import time
from tools import cancel_order, send_email

async def test_cancel_order():
    print("--- Testing cancel_order 10 times ---")
    failures = 0
    successes = 0
    
    for i in range(10):
        result = await cancel_order(f"99{i}")
        if result["status"] == "failed":
            failures += 1
        else:
            successes += 1
            
    print(f"Total Runs: 10")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Failure Rate: {(failures / 10) * 100:.0f}%")

async def test_send_email():
    print("\n--- Testing send_email latency ---")
    
    start_time = time.time()
    result = await send_email("test@example.com", "Order 9921 cancelled")
    end_time = time.time()
    
    elapsed = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed Time: {elapsed:.4f} seconds")
    
    assert 0.9 <= elapsed <= 1.5, f"Expected elapsed time ~1 second, got {elapsed}"

async def main():
    await test_cancel_order()
    await test_send_email()

if __name__ == "__main__":
    asyncio.run(main())
