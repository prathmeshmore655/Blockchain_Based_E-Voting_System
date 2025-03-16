// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    struct Voter {
        uint voterId;
        bool hasVoted;
    }

    mapping(uint => Candidate) public candidates; // Candidate ID → Candidate
    mapping(address => Voter) public voters; // Voter address → Voter info
    uint public candidatesCount;

    event VoteCasted(address indexed voter, uint voterId, uint candidateId);

    // Add a new candidate
    function addCandidate(string memory _name) public {
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
        candidatesCount++;
    }

    // Vote for a candidate
    function vote(uint _candidateId, uint _voterId) public {
        require(!voters[msg.sender].hasVoted, "You have already voted.");
        require(_candidateId < candidatesCount, "Invalid candidate ID.");

        candidates[_candidateId].voteCount++;
        voters[msg.sender] = Voter(_voterId, true);

        emit VoteCasted(msg.sender, _voterId, _candidateId);
    }

    // Get total votes for a candidate
    function getVotes(uint _candidateId) public view returns (uint) {
        require(_candidateId < candidatesCount, "Invalid candidate ID.");
        return candidates[_candidateId].voteCount;
    }

    // Get total number of candidates
    function getTotalCandidates() public view returns (uint) {
        return candidatesCount;
    }

    // Check if a voter has voted
    function hasVoterVoted(address _voter) public view returns (bool) {
        return voters[_voter].hasVoted;
    }

    // Get voter's ID
    function getVoterId(address _voter) public view returns (uint) {
        require(voters[_voter].hasVoted, "Voter has not voted yet.");
        return voters[_voter].voterId;
    }
}
