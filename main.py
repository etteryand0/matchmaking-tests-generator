from random import randint, shuffle
import os
import json
import click
import uuid


@click.command()
@click.option('--count', 
              default=1,
              prompt='Enter number of tests to generate',
              help='Number of tests to generate')
@click.option('--epoch-count', 
              default=15,
              prompt='Enter number of epochs to generate per test',
              help='Number of epochs to create per test')
@click.option('--max-user-per-epoch',
              default=20,
              prompt='Enter max number of users per epoch',
              help='Number of users per epoch')
@click.option('--max-epoch-interval',
              default=3600*4,
              prompt='Enter max time between epoch',
              help='Max time between epoches')
def generate(count, epoch_count, max_user_per_epoch, max_epoch_interval):
    dirs = list(filter(lambda x: x.startswith('test_'),os.listdir('tests')))
    
    for test_index in range(len(dirs), len(dirs) + count):
        os.mkdir(os.path.join('tests', f'test_{test_index}'))
        test_collection = {
            "00000000-0000-0000-0000-000000000000": "00000000-0000-0000-0000-000000000000"
        }
        intervals = {}
        previous_epoch = None
        
        for _ in range(epoch_count):
            epoch = []
            epoch_uuid = str(uuid.uuid4())
            if previous_epoch is None:
                epoch_uuid = '00000000-0000-0000-0000-000000000000'
            else:
                test_collection[previous_epoch] = epoch_uuid
            
            previous_epoch = epoch_uuid
            intervals[epoch_uuid] = randint(10,max_epoch_interval)
            
            for _ in range(randint(1, max_user_per_epoch + 1)):
                roles = ["top", "mid", "bot", "sup", "jungle"]
                shuffle(roles)
                user = {
                    "user_id": str(uuid.uuid4()),
                    "mmr": randint(500,10000),
                    "roles": roles,
                    "waitingTime": randint(1,100)
                }
                epoch.append(user)
            epoch_file = open(os.path.join('tests', f'test_{test_index}', f'{epoch_uuid}.json'), 'w')
            epoch_file.write(json.dumps(epoch))
            epoch_file.close()
            
        intervals_file = open(os.path.join('tests', f'test_{test_index}', 'intervals.json'), 'w')
        intervals_file.write(json.dumps(intervals))
        intervals_file.close()
        
        test_collection["last"] = epoch_uuid
        test_collection_file = open(os.path.join('tests', f'test_{test_index}', 'test.json'), 'w')
        test_collection_file.write(json.dumps(test_collection))
        test_collection_file.close()
        print(f'Created test "test_{test_index}"')

    print('Finished successfuly')


if __name__ == '__main__':
    generate()