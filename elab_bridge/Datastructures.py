import os
import os


def creat_repository_by_experiments(root_to_save, data_type='micr', sub_id=None, sess_id=None):
    subject_dir = os.path.join(root_to_save, str(sub_id))
    session_dir = os.path.join(subject_dir, str(sess_id))

    if not os.path.exists(subject_dir):
        os.makedirs(subject_dir)

    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    if not os.path.exists(os.path.join(session_dir, data_type)):
        os.makedirs(os.path.join(session_dir, data_type))


def main():
    root_directory = "."
    subject_id = "sujet1"
    session_id = "session1"
    data_type = "type_de_donnees"

    creat_repository_by_experiments(root_directory, data_type, subject_id, session_id)


if __name__ == "__main__":
    main()
