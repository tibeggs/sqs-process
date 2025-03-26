import json
import time
import signal
import sys
import traceback
from database.connection import get_db
from sqs.client import SQSClient

class SQSProcessor:
    def __init__(self):
        self.running = True
        self.sqs_client = SQSClient()
        self.db = get_db()
        self.poll_interval = 5  # Seconds between polls when no messages
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle shutdown signals gracefully"""
        print("\nShutdown signal received. Finishing current processing and exiting...")
        self.running = False

    def process_message(self, message):
        try:
            message_body = message['Body']
            print(f"Message body: {message_body}")
            
            # Convert timestamp from milliseconds to datetime
            message_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', 
                time.localtime(int(message['Attributes']['SentTimestamp']) / 1000)
            )
            print(f"Message time: {message_time}")
            print(self.db)
            
            cursor = self.db.cursor()

            sql = """
                INSERT INTO extable 
                (message, message_time) 
                VALUES (%s, %s)
            """
            cursor.execute(sql, (message_body, message_time))
            cursor.close()
            
            self.db.commit()
            return True
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            print("Full traceback:")
            traceback.print_exc()
            return False

    def run(self):
        print("SQS processor started. Press Ctrl+C to exit.")
        
        while self.running:
            try:
                messages = self.sqs_client.receive_message()
                
                if messages:
                    print(f"Received {len(messages)} messages")
                    for message in messages:
                        if not self.running:
                            break
                        print(f"Processing message: {message['MessageId']}")
                        print(message['Body'])
                        
                        success = self.process_message(message)
                        
                        if success:
                            self.sqs_client.delete_message(message['ReceiptHandle'])
                            print("Message processed and deleted successfully")
                        else:
                            print("Failed to process message")
                else:
                    print(f"No messages found. Polling again in {self.poll_interval} seconds...")
                    
                # Sleep between polls to avoid excessive API calls
                time.sleep(self.poll_interval)

            except Exception as e:
                print(f"Error: {str(e)}")
                print("Full traceback:")
                traceback.print_exc()
                time.sleep(self.poll_interval)
        
        print("SQS processor shutting down")
        self.db.close()

def main():
    processor = SQSProcessor()
    processor.run()

if __name__ == "__main__":
    main()