from random import randint, sample
import os
import json
import click
import uuid

roles = ["top", "mid", "bot", "sup", "jungle"]


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
def generate(count, epoch_count, max_user_per_epoch):
    dirs = list(filter(lambda x: x.startswith('test_'),os.listdir('tests')))
    
    for test_index in range(len(dirs), len(dirs) + count):
        os.mkdir(os.path.join('tests', f'test_{test_index}'))
        test_collection = {}
        previous_epoch = None
        
        for _ in range(epoch_count):
            epoch = []
            epoch_uuid = str(uuid.uuid4())
            if previous_epoch is None:
                epoch_uuid = '00000000-0000-0000-0000-000000000000'
            else:
                test_collection[previous_epoch] = epoch_uuid
            
            previous_epoch = epoch_uuid
            
            for _ in range(randint(1, max_user_per_epoch + 1)):
                user = {
                    "user_id": str(uuid.uuid4()),
                    "mmr": randint(500,10000),
                    "roles": sample(roles, randint(1,5)),
                    "waitingTime": randint(1,100)
                }
                epoch.append(user)
            epoch_file = open(os.path.join('tests', f'test_{test_index}', f'{epoch_uuid}.json'), 'w')
            epoch_file.write(json.dumps(epoch))
            epoch_file.close()
        
        test_collection[epoch_uuid] = '00000000-0000-0000-0000-000000000000'
        test_collection_file = open(os.path.join('tests', f'test_{test_index}', 'test.json'), 'w')
        test_collection_file.write(json.dumps(test_collection))
        test_collection_file.close()
        print(f'Created test "test_{test_index}"')

    print('Finished successfuly')


if __name__ == '__main__':
    generate()